import json
import asyncio
import aiofiles
import time
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from discord_notifier import DiscordNotifier
from notification_manager import NotificationManager
from real_time_data_manager import RealTimeDataManager
from performance_optimizer import PerformanceOptimizer

# Load notification config from JSON file
CONFIG_FILE = Path("config/notification_config.json")
def load_config():
    """
    Load configuration from the config file, or use fallback defaults if missing or invalid.
    Returns:
        dict: Configuration dictionary.
    """
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        # Fallback defaults
        return {
            "threshold": 200,
            "check_interval": 60,
            "notification_channels": ["console"],
            "discord_webhook_url": "",
            "throttle_minutes": 30,
            "real_time_data": {
                "enabled": True,
                "refresh_interval": 300,
                "data_directory": "data",
                "auto_refresh": True
            }
        }

# Load configuration
config = load_config()
PRICE_FILE = Path("src/data/flight_prices.json")
THRESHOLD = config.get("threshold", 200)
CHECK_INTERVAL = config.get("check_interval", 60)
CHANNELS = config.get("notification_channels", ["console"])
DISCORD_WEBHOOK_URL = config.get("discord_webhook_url", "")
THROTTLE_MINUTES = config.get("throttle_minutes", 30)

# Real-time data configuration
real_time_config = config.get("real_time_data", {})
REAL_TIME_ENABLED = real_time_config.get("enabled", True)
REFRESH_INTERVAL = real_time_config.get("refresh_interval", 300)
DATA_DIRECTORY = real_time_config.get("data_directory", "data")

# Performance optimization configuration
performance_config = config.get("performance", {})
performance_config.update({
    "check_interval": CHECK_INTERVAL,
    "min_sleep_interval": config.get("min_sleep_interval", 30),
    "max_sleep_interval": config.get("max_sleep_interval", 600),
    "adaptive_sleep": config.get("adaptive_sleep", True),
    "memory_threshold": config.get("memory_threshold", 80),
    "memory_monitoring": config.get("memory_monitoring", True),
    "cache_ttl": config.get("cache_ttl", 300)
})

# Initialize notification and data managers
# DiscordNotifier: sends notifications to Discord if enabled
# NotificationManager: handles throttling and notification history
# RealTimeDataManager: manages real-time data refresh and caching
# PerformanceOptimizer: handles sleep tuning, memory monitoring, and graceful shutdown

discord_notifier = DiscordNotifier(DISCORD_WEBHOOK_URL) if "discord" in CHANNELS and DISCORD_WEBHOOK_URL else None
notification_manager = NotificationManager(throttle_minutes=THROTTLE_MINUTES)
data_manager = RealTimeDataManager(data_dir=DATA_DIRECTORY, refresh_interval=REFRESH_INTERVAL) if REAL_TIME_ENABLED else None
performance_optimizer = PerformanceOptimizer(performance_config)

async def load_prices():
    """
    Load flight prices using the real-time data manager if enabled, otherwise use efficient file-based loading.
    Returns:
        list: List of flight price dicts.
    """
    if data_manager and REAL_TIME_ENABLED:
        # Use real-time data manager for up-to-date, cached data
        return await data_manager.get_all_flight_data()
    else:
        # Use performance optimizer for efficient file-based loading
        return await performance_optimizer.efficient_data_load(PRICE_FILE, "flight_prices")

async def send_notification(flight):
    """
    Send notification for a price drop asynchronously (console and/or Discord), with throttling and history tracking.
    Args:
        flight (dict): Flight information dict.
    Returns:
        str or None: Notification message if sent, else None.
    """
    # Throttle repeated notifications for the same flight
    if notification_manager.is_throttled(flight):
        print(f"⏸️  Skipping notification (throttled): {flight.get('airline', 'Unknown')} to {flight.get('destination', 'Unknown')} at ${flight.get('price', 0)}")
        return None
    
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{timestamp}] 🎉 Price drop! {flight['airline']} to {flight['destination']} at ${flight['price']}"
    channels_used = []
    
    # Console notification
    if "console" in CHANNELS:
        print(message)
        channels_used.append("console")
    
    # Discord notification (if enabled)
    if discord_notifier:
        success = await discord_notifier.send_notification(flight)
        if success:
            channels_used.append("discord")
    
    # Record the notification in history
    notification_manager.record_notification(flight, channels_used)
    
    # Track notification performance
    duration = time.time() - start_time
    performance_optimizer.track_notification_time("price_drop", duration)
    
    return message

async def data_change_callback(new_data):
    """
    Callback function called when new data is available from the real-time data manager.
    Args:
        new_data (list): List of new flight data dicts.
    """
    print(f"📊 New data available: {len(new_data)} flights")
    
    # Check for price drops in new data
    notifications_sent = 0
    for flight in new_data:
        try:
            price = float(flight.get("price", float('inf')))
            if price < THRESHOLD:
                result = await send_notification(flight)
                if result:
                    notifications_sent += 1
        except Exception as e:
            print(f"❌ Error processing flight entry: {e}")
    
    if notifications_sent > 0:
        print(f"📊 Sent {notifications_sent} notification(s) from new data")

async def monitor_prices(threshold=THRESHOLD, interval=CHECK_INTERVAL):
    """
    Main async monitoring loop. Checks for price drops and sends notifications.
    Integrates real-time data, notification throttling, performance optimization, and graceful shutdown.
    Args:
        threshold (float): Price threshold for notifications.
        interval (int): How often to check prices (seconds).
    """
    print(f"🚀 Starting async price monitoring...")
    print(f"💰 Threshold: ${threshold}")
    print(f"⏱️  Check interval: {interval} seconds")
    print(f"🔔 Channels: {CHANNELS}")
    print(f"⏸️  Throttle: {notification_manager.throttle_minutes} minutes")
    
    if REAL_TIME_ENABLED and data_manager:
        print(f"🔄 Real-time data enabled (refresh: {REFRESH_INTERVAL}s)")
        print(f"📁 Data directory: {DATA_DIRECTORY}")
    else:
        print(f"📁 Monitoring: {PRICE_FILE}")
    
    # Performance optimization info
    print(f"⚡ Performance optimization: {'enabled' if performance_optimizer.adaptive_sleep else 'disabled'}")
    print(f"💾 Memory monitoring: {'enabled' if performance_optimizer.memory_monitor_enabled else 'disabled'}")
    print(f"🔄 Adaptive sleep: {performance_optimizer.min_sleep_interval}s - {performance_optimizer.max_sleep_interval}s")
    
    print("-" * 50)
    
    # Show notification stats on startup
    stats = notification_manager.get_notification_stats()
    print(f"📊 Notification stats: {stats['total']} total, {stats['today']} today, {stats['this_week']} this week")
    
    if data_manager:
        data_stats = data_manager.get_data_stats()
        print(f"📊 Data stats: {data_stats['total_routes']} routes, {data_stats['total_flights']} flights cached")
    
    # Register cleanup callbacks for graceful shutdown
    performance_optimizer.add_cleanup_callback(lambda: print("📊 Final performance summary:"))
    performance_optimizer.add_cleanup_callback(performance_optimizer.print_performance_summary)
    
    # Real-time data monitoring mode
    if REAL_TIME_ENABLED and data_manager:
        # Start data monitoring in background
        data_monitor_task = asyncio.create_task(
            data_manager.monitor_data_changes(data_change_callback)
        )
        
        # Main monitoring loop (simplified since data monitoring handles updates)
        while not performance_optimizer.shutdown_requested:
            try:
                # Use optimized sleep
                should_continue = await performance_optimizer.optimized_sleep(
                    interval, notifications_sent=0, data_changed=False
                )
                if not should_continue:
                    break
                
                # Check if data monitor is still running
                if data_monitor_task.done():
                    print("❌ Data monitor task ended, restarting...")
                    data_monitor_task = asyncio.create_task(
                        data_manager.monitor_data_changes(data_change_callback)
                    )
                    
            except Exception as e:
                print(f"❌ Error in monitoring loop: {e}")
                await asyncio.sleep(interval)
    else:
        # Traditional file-based monitoring with performance optimization
        while not performance_optimizer.shutdown_requested:
            try:
                prices = await load_prices()
                notifications_sent = 0
                data_changed = len(prices) > 0  # Simple heuristic for data change
                
                for flight in prices:
                    try:
                        price = float(flight.get("price", float('inf')))
                        airline = flight.get("airline", "Unknown")
                        destination = flight.get("destination", "Unknown")
                        
                        if price < threshold:
                            result = await send_notification(flight)
                            if result:  # Only count if not throttled
                                notifications_sent += 1
                            
                    except Exception as e:
                        print(f"❌ Error processing flight entry: {e}")
                
                if notifications_sent > 0:
                    print(f"📊 Sent {notifications_sent} notification(s) this cycle")
                
                # Use optimized sleep with activity tracking
                should_continue = await performance_optimizer.optimized_sleep(
                    interval, notifications_sent=notifications_sent, data_changed=data_changed
                )
                if not should_continue:
                    break
                
            except Exception as e:
                print(f"❌ Error in monitoring loop: {e}")
                await asyncio.sleep(interval)  # Continue monitoring even after errors
    
    # Perform cleanup on exit
    await performance_optimizer.perform_cleanup()

async def main():
    """
    Main entry point for the async price monitoring agent.
    Handles top-level error handling and ensures cleanup on exit.
    """
    try:
        await monitor_prices()
    except KeyboardInterrupt:
        print("\n🛑 Price monitoring stopped by user")
        # Graceful shutdown is handled by performance optimizer
    except Exception as e:
        print(f"❌ Fatal error in main: {e}")
        # Ensure cleanup happens even on error
        await performance_optimizer.perform_cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 