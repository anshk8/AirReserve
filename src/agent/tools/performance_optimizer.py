import asyncio
import psutil
import time
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
import threading
import signal
import sys

class PerformanceOptimizer:
    """
    Handles performance optimization for the price monitoring agent.
    Features:
      - Adaptive sleep interval tuning based on activity
      - Efficient data loading with caching and TTL
      - Memory and CPU usage monitoring
      - Graceful shutdown with cleanup callbacks
      - Performance metrics tracking and export
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the optimizer with configuration.
        Args:
            config (Dict): Performance-related configuration options.
        """
        self.config = config or {}
        
        # Performance settings
        self.min_sleep_interval = self.config.get("min_sleep_interval", 30)  # Minimum sleep interval (seconds)
        self.max_sleep_interval = self.config.get("max_sleep_interval", 600)  # Maximum sleep interval (seconds)
        self.adaptive_sleep = self.config.get("adaptive_sleep", True)  # Enable adaptive sleep
        self.memory_threshold = self.config.get("memory_threshold", 80)  # Memory usage threshold (%)
        
        # Performance tracking
        self.performance_metrics = {
            "data_load_times": [],  # List of data load timing records
            "notification_times": [],  # List of notification timing records
            "memory_usage": [],  # List of memory usage snapshots
            "cpu_usage": [],  # List of CPU usage snapshots
            "sleep_intervals": [],  # List of sleep interval changes
            "start_time": time.time()  # Agent start time
        }
        
        # Adaptive sleep variables
        self.current_sleep_interval = self.config.get("check_interval", 60)
        self.activity_level = 0  # 0-100, higher means more activity
        self.last_activity_time = time.time()
        
        # Graceful shutdown
        self.shutdown_requested = False
        self.cleanup_callbacks = []  # List of cleanup functions to call on shutdown
        self._setup_signal_handlers()
        
        # Data caching
        self.data_cache = {}  # In-memory cache for loaded data
        self.cache_timestamps = {}  # Cache entry timestamps
        self.cache_ttl = self.config.get("cache_ttl", 300)  # Cache time-to-live (seconds)
        
        # Memory monitoring
        self.memory_monitor_enabled = self.config.get("memory_monitoring", True)
        self.last_memory_check = 0
        self.memory_check_interval = 60  # How often to check memory (seconds)
    
    def _setup_signal_handlers(self):
        """
        Setup signal handlers for SIGINT and SIGTERM to enable graceful shutdown.
        """
        def signal_handler(signum, frame):
            print(f"\n🛑 Received signal {signum}, initiating graceful shutdown...")
            self.request_shutdown()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def request_shutdown(self):
        """
        Request a graceful shutdown. Sets a flag checked by main loops.
        """
        self.shutdown_requested = True
    
    def add_cleanup_callback(self, callback: Callable):
        """
        Register a function to be called during shutdown cleanup.
        Args:
            callback (Callable): Function or coroutine to call on shutdown.
        """
        self.cleanup_callbacks.append(callback)
    
    async def perform_cleanup(self):
        """
        Run all registered cleanup callbacks and save performance metrics.
        """
        print("🧹 Performing cleanup operations...")
        
        for callback in self.cleanup_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback()
                else:
                    callback()
            except Exception as e:
                print(f"❌ Error in cleanup callback: {e}")
        
        # Save performance metrics to file
        await self.save_performance_metrics()
        print("✅ Cleanup completed")
    
    def optimize_sleep_interval(self, notifications_sent: int = 0, data_changed: bool = False) -> int:
        """
        Dynamically adjust the sleep interval based on recent activity.
        Args:
            notifications_sent (int): Number of notifications sent in last cycle.
            data_changed (bool): Whether new data was detected.
        Returns:
            int: Optimized sleep interval in seconds.
        """
        if not self.adaptive_sleep:
            return self.current_sleep_interval
        
        # Update activity level based on recent activity
        current_time = time.time()
        time_since_activity = current_time - self.last_activity_time
        
        # Increase activity level if there was activity
        if notifications_sent > 0 or data_changed:
            self.activity_level = min(100, self.activity_level + 20)
            self.last_activity_time = current_time
        else:
            # Gradually decrease activity level over time
            decay_rate = 5  # Decrease by 5 points per minute of inactivity
            decay_amount = (time_since_activity / 60) * decay_rate
            self.activity_level = max(0, self.activity_level - decay_amount)
        
        # Calculate optimal sleep interval based on activity
        if self.activity_level > 80:
            optimal_interval = self.min_sleep_interval  # High activity: check frequently
        elif self.activity_level > 50:
            optimal_interval = (self.min_sleep_interval + self.max_sleep_interval) // 2  # Medium
        else:
            optimal_interval = self.max_sleep_interval  # Low activity: check less often
        
        # Smooth transition to avoid sudden jumps
        change_rate = 0.1  # 10% change per cycle
        if optimal_interval > self.current_sleep_interval:
            self.current_sleep_interval = min(optimal_interval, 
                                            self.current_sleep_interval * (1 + change_rate))
        else:
            self.current_sleep_interval = max(optimal_interval, 
                                            self.current_sleep_interval * (1 - change_rate))
        
        # Clamp to allowed range
        self.current_sleep_interval = max(self.min_sleep_interval, 
                                        min(self.max_sleep_interval, 
                                            int(self.current_sleep_interval)))
        
        # Track sleep intervals for metrics
        self.performance_metrics["sleep_intervals"].append({
            "timestamp": current_time,
            "interval": self.current_sleep_interval,
            "activity_level": self.activity_level,
            "notifications_sent": notifications_sent,
            "data_changed": data_changed
        })
        
        return self.current_sleep_interval
    
    async def efficient_data_load(self, file_path: Path, cache_key: str = None) -> List[Dict]:
        """
        Load data from file efficiently, using in-memory cache with TTL if possible.
        Args:
            file_path (Path): Path to the data file.
            cache_key (str): Optional cache key for this data.
        Returns:
            List[Dict]: Loaded data (empty list on error).
        """
        start_time = time.time()
        
        # Return cached data if valid
        if cache_key and cache_key in self.data_cache:
            cache_time = self.cache_timestamps.get(cache_key, 0)
            if time.time() - cache_time < self.cache_ttl:
                load_time = time.time() - start_time
                self.performance_metrics["data_load_times"].append({
                    "timestamp": start_time,
                    "load_time": load_time,
                    "source": "cache",
                    "cache_key": cache_key
                })
                return self.data_cache[cache_key]
        
        try:
            # Check if file exists
            if not file_path.exists():
                return []
            
            file_mtime = file_path.stat().st_mtime
            
            # Load data from file (thread-safe)
            async with asyncio.Lock():
                with open(file_path, 'r') as f:
                    data = json.load(f)
            
            # Cache the data
            if cache_key:
                self.data_cache[cache_key] = data
                self.cache_timestamps[cache_key] = time.time()
            
            load_time = time.time() - start_time
            self.performance_metrics["data_load_times"].append({
                "timestamp": start_time,
                "load_time": load_time,
                "source": "file",
                "file_size": file_path.stat().st_size,
                "cache_key": cache_key
            })
            
            return data
            
        except Exception as e:
            print(f"❌ Error in efficient data load: {e}")
            return []
    
    def check_memory_usage(self) -> Dict[str, float]:
        """
        Check and record current process and system memory/CPU usage.
        Returns:
            Dict[str, float]: Memory and CPU usage metrics.
        """
        if not self.memory_monitor_enabled:
            return {}
        
        current_time = time.time()
        if current_time - self.last_memory_check < self.memory_check_interval:
            return {}
        
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            memory_percent = process.memory_percent()
            cpu_percent = process.cpu_percent()
            
            # Get system memory info
            system_memory = psutil.virtual_memory()
            
            metrics = {
                "process_memory_mb": memory_info.rss / 1024 / 1024,
                "process_memory_percent": memory_percent,
                "process_cpu_percent": cpu_percent,
                "system_memory_percent": system_memory.percent,
                "system_memory_available_gb": system_memory.available / 1024 / 1024 / 1024
            }
            
            # Track metrics
            self.performance_metrics["memory_usage"].append({
                "timestamp": current_time,
                **metrics
            })
            
            self.performance_metrics["cpu_usage"].append({
                "timestamp": current_time,
                "cpu_percent": cpu_percent
            })
            
            self.last_memory_check = current_time
            
            # If memory usage is too high, clear caches
            if memory_percent > self.memory_threshold:
                print(f"⚠️  High memory usage: {memory_percent:.1f}%")
                self._handle_high_memory_usage()
            
            return metrics
            
        except Exception as e:
            print(f"❌ Error checking memory usage: {e}")
            return {}
    
    def _handle_high_memory_usage(self):
        """
        Handle high memory usage by clearing caches and trimming metrics.
        """
        print("🧹 Clearing caches due to high memory usage...")
        
        # Clear data cache
        cache_size_before = len(self.data_cache)
        self.data_cache.clear()
        self.cache_timestamps.clear()
        
        # Trim old performance metrics (keep last 100 entries)
        for key in ["data_load_times", "notification_times", "memory_usage", "cpu_usage", "sleep_intervals"]:
            if len(self.performance_metrics[key]) > 100:
                self.performance_metrics[key] = self.performance_metrics[key][-100:]
        
        print(f"✅ Cleared {cache_size_before} cached items")
    
    def track_notification_time(self, notification_type: str, duration: float):
        """
        Record the time taken to send a notification for performance metrics.
        Args:
            notification_type (str): Type of notification sent.
            duration (float): Time taken in seconds.
        """
        self.performance_metrics["notification_times"].append({
            "timestamp": time.time(),
            "type": notification_type,
            "duration": duration
        })
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Summarize and return current performance statistics.
        Returns:
            Dict[str, Any]: Summary of performance metrics and stats.
        """
        current_time = time.time()
        uptime = current_time - self.performance_metrics["start_time"]
        
        # Calculate averages
        avg_load_time = 0
        if self.performance_metrics["data_load_times"]:
            avg_load_time = sum(m["load_time"] for m in self.performance_metrics["data_load_times"]) / len(self.performance_metrics["data_load_times"])
        
        avg_notification_time = 0
        if self.performance_metrics["notification_times"]:
            avg_notification_time = sum(m["duration"] for m in self.performance_metrics["notification_times"]) / len(self.performance_metrics["notification_times"])
        
        avg_sleep_interval = 0
        if self.performance_metrics["sleep_intervals"]:
            avg_sleep_interval = sum(m["interval"] for m in self.performance_metrics["sleep_intervals"]) / len(self.performance_metrics["sleep_intervals"])
        
        # Get recent memory usage
        recent_memory = self.performance_metrics["memory_usage"][-1] if self.performance_metrics["memory_usage"] else {}
        
        return {
            "uptime_seconds": uptime,
            "uptime_formatted": str(timedelta(seconds=int(uptime))),
            "current_sleep_interval": self.current_sleep_interval,
            "activity_level": self.activity_level,
            "cache_size": len(self.data_cache),
            "avg_data_load_time": avg_load_time,
            "avg_notification_time": avg_notification_time,
            "avg_sleep_interval": avg_sleep_interval,
            "total_data_loads": len(self.performance_metrics["data_load_times"]),
            "total_notifications": len(self.performance_metrics["notification_times"]),
            "memory_usage_mb": recent_memory.get("process_memory_mb", 0),
            "memory_usage_percent": recent_memory.get("process_memory_percent", 0),
            "cpu_usage_percent": recent_memory.get("process_cpu_percent", 0)
        }
    
    async def save_performance_metrics(self):
        """
        Save all collected performance metrics and final stats to a JSON file.
        """
        try:
            metrics_file = Path("data/performance_metrics.json")
            metrics_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Add final stats
            final_stats = self.get_performance_stats()
            
            metrics_data = {
                "performance_metrics": self.performance_metrics,
                "final_stats": final_stats,
                "exported_at": datetime.now().isoformat()
            }
            
            with open(metrics_file, 'w') as f:
                json.dump(metrics_data, f, indent=2, default=str)
            
            print(f"📊 Performance metrics saved to {metrics_file}")
            
        except Exception as e:
            print(f"❌ Error saving performance metrics: {e}")
    
    async def optimized_sleep(self, base_interval: int, notifications_sent: int = 0, data_changed: bool = False) -> bool:
        """
        Sleep for an optimized interval, checking for shutdown and memory usage.
        Args:
            base_interval (int): Base interval to use for sleep.
            notifications_sent (int): Number of notifications sent in last cycle.
            data_changed (bool): Whether new data was detected.
        Returns:
            bool: True if should continue, False if shutdown requested.
        """
        if self.shutdown_requested:
            return False
        
        # Optimize sleep interval
        optimized_interval = self.optimize_sleep_interval(notifications_sent, data_changed)
        
        # Check memory usage before sleep
        memory_metrics = self.check_memory_usage()
        
        # Sleep in small chunks to allow for quick shutdown
        chunk_size = min(optimized_interval, 10)  # Max 10 seconds per chunk
        remaining_time = optimized_interval
        
        while remaining_time > 0 and not self.shutdown_requested:
            sleep_time = min(chunk_size, remaining_time)
            await asyncio.sleep(sleep_time)
            remaining_time -= sleep_time
        
        return not self.shutdown_requested
    
    def print_performance_summary(self):
        """
        Print a summary of current performance metrics to the console.
        """
        stats = self.get_performance_stats()
        
        print("\n" + "="*60)
        print("📊 PERFORMANCE SUMMARY")
        print("="*60)
        print(f"⏱️  Uptime: {stats['uptime_formatted']}")
        print(f"💤 Current sleep interval: {stats['current_sleep_interval']}s")
        print(f"📈 Activity level: {stats['activity_level']:.1f}/100")
        print(f"💾 Cache size: {stats['cache_size']} items")
        print(f"📊 Memory usage: {stats['memory_usage_mb']:.1f} MB ({stats['memory_usage_percent']:.1f}%)")
        print(f"🖥️  CPU usage: {stats['cpu_usage_percent']:.1f}%")
        print(f"⚡ Avg data load time: {stats['avg_data_load_time']:.3f}s")
        print(f"🔔 Avg notification time: {stats['avg_notification_time']:.3f}s")
        print(f"📈 Total data loads: {stats['total_data_loads']}")
        print(f"📈 Total notifications: {stats['total_notifications']}")
        print("="*60) 