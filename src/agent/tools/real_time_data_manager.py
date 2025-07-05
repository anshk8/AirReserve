import asyncio
import aiofiles
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import threading
from src.agent.tools.tavily_price_tracker import tavily_price_tracker

class RealTimeDataManager:
    """Manages real-time flight data updates with concurrent access safety."""
    
    def __init__(self, data_dir="data", refresh_interval=300):  # 5 minutes default
        self.data_dir = Path(data_dir)
        self.refresh_interval = refresh_interval
        self.last_refresh = {}  # Track last refresh per route
        self.data_cache = {}  # In-memory cache
        self.file_locks = {}  # Thread locks for file access
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_file_lock(self, filename: str) -> threading.Lock:
        """Get or create a thread lock for a specific file."""
        if filename not in self.file_locks:
            self.file_locks[filename] = threading.Lock()
        return self.file_locks[filename]
    
    async def load_flight_data(self, from_city: str, to_city: str) -> List[Dict]:
        """Load flight data for a specific route with caching."""
        filename = f"flight_prices_{from_city}_{to_city}.json"
        file_path = self.data_dir / filename
        
        # Check if we need to refresh data
        if self._should_refresh_data(from_city, to_city):
            await self._refresh_flight_data(from_city, to_city)
        
        # Load from cache or file
        cache_key = f"{from_city}_{to_city}"
        if cache_key in self.data_cache:
            return self.data_cache[cache_key]
        
        # Load from file with thread safety
        lock = self._get_file_lock(filename)
        with lock:
            try:
                if file_path.exists():
                    async with aiofiles.open(file_path, 'r') as f:
                        content = await f.read()
                        data = json.loads(content)
                        
                        # Extract latest flights from the most recent search
                        if data.get("searches"):
                            latest_search = data["searches"][-1]
                            flights = latest_search.get("flights", [])
                            
                            # Cache the data
                            self.data_cache[cache_key] = flights
                            return flights
                        
                        return []
                else:
                    return []
                    
            except Exception as e:
                print(f"❌ Error loading flight data for {from_city} to {to_city}: {e}")
                return []
    
    def _should_refresh_data(self, from_city: str, to_city: str) -> bool:
        """Check if data should be refreshed based on last refresh time."""
        route_key = f"{from_city}_{to_city}"
        last_refresh_time = self.last_refresh.get(route_key)
        
        if not last_refresh_time:
            return True
        
        time_since_refresh = time.time() - last_refresh_time
        return time_since_refresh > self.refresh_interval
    
    async def _refresh_flight_data(self, from_city: str, to_city: str):
        """Refresh flight data using Tavily API."""
        print(f"🔄 Refreshing flight data for {from_city} to {to_city}...")
        
        try:
            # Use the existing Tavily price tracker
            params = {
                "FROM": from_city,
                "TO": to_city,
                "maxPrice": 1000  # High threshold to get all flights
            }
            
            # Call the Tavily API (this is synchronous, so we run it in executor)
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, tavily_price_tracker, params)
            
            # Update last refresh time
            route_key = f"{from_city}_{to_city}"
            self.last_refresh[route_key] = time.time()
            
            print(f"✅ Data refresh completed for {from_city} to {to_city}")
            
        except Exception as e:
            print(f"❌ Error refreshing data for {from_city} to {to_city}: {e}")
    
    async def get_all_flight_data(self) -> List[Dict]:
        """Get all available flight data from all routes."""
        all_flights = []
        
        # Get all flight price files
        flight_files = list(self.data_dir.glob("flight_prices_*.json"))
        
        for file_path in flight_files:
            try:
                # Extract route from filename
                filename = file_path.stem
                parts = filename.replace("flight_prices_", "").split("_")
                if len(parts) >= 2:
                    from_city = parts[0]
                    to_city = parts[1]
                    
                    flights = await self.load_flight_data(from_city, to_city)
                    all_flights.extend(flights)
                    
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
        
        return all_flights
    
    async def monitor_data_changes(self, callback):
        """Monitor for data changes and call callback when new data is available."""
        print(f"👀 Starting data change monitoring (refresh interval: {self.refresh_interval}s)")
        
        while True:
            try:
                # Get current data
                current_data = await self.get_all_flight_data()
                
                # Call callback with new data
                if callback:
                    await callback(current_data)
                
                # Wait for next refresh cycle
                await asyncio.sleep(self.refresh_interval)
                
            except Exception as e:
                print(f"❌ Error in data monitoring: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    def get_data_stats(self) -> Dict:
        """Get statistics about the data."""
        stats = {
            "total_routes": 0,
            "total_flights": 0,
            "last_refresh_times": {},
            "cache_hits": len(self.data_cache)
        }
        
        flight_files = list(self.data_dir.glob("flight_prices_*.json"))
        stats["total_routes"] = len(flight_files)
        
        for file_path in flight_files:
            try:
                filename = file_path.stem
                parts = filename.replace("flight_prices_", "").split("_")
                if len(parts) >= 2:
                    from_city = parts[0]
                    to_city = parts[1]
                    route_key = f"{from_city}_{to_city}"
                    
                    # Get last refresh time
                    last_refresh = self.last_refresh.get(route_key, 0)
                    if last_refresh > 0:
                        stats["last_refresh_times"][route_key] = datetime.fromtimestamp(last_refresh).isoformat()
                    
                    # Count flights in cache
                    if route_key in self.data_cache:
                        stats["total_flights"] += len(self.data_cache[route_key])
                        
            except Exception as e:
                print(f"❌ Error getting stats for {file_path}: {e}")
        
        return stats
    
    async def force_refresh_all(self):
        """Force refresh all available routes."""
        print("🔄 Forcing refresh of all flight data...")
        
        flight_files = list(self.data_dir.glob("flight_prices_*.json"))
        
        for file_path in flight_files:
            try:
                filename = file_path.stem
                parts = filename.replace("flight_prices_", "").split("_")
                if len(parts) >= 2:
                    from_city = parts[0]
                    to_city = parts[1]
                    await self._refresh_flight_data(from_city, to_city)
                    
            except Exception as e:
                print(f"❌ Error refreshing {file_path}: {e}")
        
        print("✅ Force refresh completed") 