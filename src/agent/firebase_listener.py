"""
Firebase Real-time Listener for Flight Searches
Monitors Firebase for new flight search entries and triggers MCP agent with Tavily API calls
"""

import os
import time
import json
import requests
import threading
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Import tools for processing
from .tools.tavily_price_tracker import tavily_price_tracker
from .tools.databaseTools import _get_flight_searches_impl

# Load environment variables
load_dotenv()

class FirebaseListener:
    def __init__(self):
        self.database_url = os.environ.get("FIREBASE_DATABASE_URL")
        self.last_processed_timestamp = None
        self.is_running = False
        self.listener_thread = None
        self.processed_records = set()  # Track processed record IDs
        
        if not self.database_url or self.database_url == "https://your-project-default-rtdb.firebaseio.com/":
            raise ValueError("Firebase Database URL not configured. Please update FIREBASE_DATABASE_URL in your .env file.")
    
    def start_listening(self, poll_interval: int = 5):
        """
        Start listening for new Firebase entries
        
        Args:
            poll_interval: Seconds between polling Firebase (default: 5)
        """
        if self.is_running:
            print("⚠️ Listener is already running!")
            return
        
        print(f"🔥 Starting Firebase listener (polling every {poll_interval}s)")
        print(f"📡 Monitoring: {self.database_url.rstrip('/')}/flight_searches.json")
        
        self.is_running = True
        self.listener_thread = threading.Thread(
            target=self._listen_loop,
            args=(poll_interval,),
            daemon=True
        )
        self.listener_thread.start()
    
    def stop_listening(self):
        """Stop the Firebase listener"""
        if not self.is_running:
            print("⚠️ Listener is not running!")
            return
        
        print("🛑 Stopping Firebase listener...")
        self.is_running = False
        if self.listener_thread:
            self.listener_thread.join(timeout=10)
        print("✅ Firebase listener stopped")
    
    def _listen_loop(self, poll_interval: int):
        """Main listening loop that polls Firebase"""
        while self.is_running:
            try:
                # Check for new entries
                new_entries = self._get_new_entries()
                
                if new_entries:
                    print(f"🆕 Found {len(new_entries)} new flight search(es)")
                    for entry in new_entries:
                        self._process_flight_search(entry)
                
                # Wait before next poll
                time.sleep(poll_interval)
                
            except Exception as e:
                print(f"❌ Error in listener loop: {str(e)}")
                time.sleep(poll_interval)  # Wait before retrying
    
    def _get_new_entries(self) -> list:
        """Get new flight search entries from Firebase"""
        try:
            url = f"{self.database_url.rstrip('/')}/flight_searches.json"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ Firebase request failed: {response.status_code}")
                return []
            
            all_data = response.json()
            if not all_data:
                return []
            
            new_entries = []
            for record_id, search_data in all_data.items():
                # Skip if we've already processed this record
                if record_id in self.processed_records:
                    continue
                
                # Add record ID to the data
                search_data["record_id"] = record_id
                new_entries.append(search_data)
                
                # Mark as processed
                self.processed_records.add(record_id)
            
            return new_entries
            
        except Exception as e:
            print(f"❌ Error fetching Firebase data: {str(e)}")
            return []
    
    def _process_flight_search(self, entry: Dict[str, Any]):
        """
        Process a new flight search entry by calling Tavily API through the agent
        
        Args:
            entry: Flight search entry from Firebase
        """
        try:
            record_id = entry.get("record_id", "unknown")
            to_destination = entry.get("to", "")
            from_origin = entry.get("from", "")
            max_price = entry.get("maxPrice", 0)
            user_id = entry.get("userId", "default")
            timestamp = entry.get("timestamp", "")
            
            print(f"\n🎯 Processing flight search {record_id}")
            print(f"   📍 Route: {from_origin} → {to_destination}")
            print(f"   💰 Max Price: ${max_price}")
            print(f"   👤 User: {user_id}")
            print(f"   ⏰ Created: {timestamp}")
            
            # Validate required fields
            if not all([to_destination, from_origin, max_price]):
                print(f"❌ Missing required fields in record {record_id}")
                return
            
            # Call Tavily API through the price tracker tool
            print(f"🔍 Calling Tavily API for flight prices...")
            
            result = tavily_price_tracker.invoke({
                "from_city": from_origin,
                "to_city": to_destination,
                "max_price": str(max_price)
            })
            
            print(f"📋 Tavily API Result:")
            print(f"   {result}")
            
            # You could also save results back to Firebase or trigger notifications here
            self._save_processing_result(record_id, result, entry)
            
        except Exception as e:
            print(f"❌ Error processing flight search {entry.get('record_id', 'unknown')}: {str(e)}")
    
    def _save_processing_result(self, record_id: str, tavily_result: str, original_entry: Dict[str, Any]):
        """
        Save the processing result back to Firebase or log it
        
        Args:
            record_id: Firebase record ID
            tavily_result: Result from Tavily API call
            original_entry: Original flight search entry
        """
        try:
            # Create processing result record
            processing_data = {
                "original_search_id": record_id,
                "tavily_result": tavily_result,
                "processed_at": datetime.now().isoformat(),
                "original_search": original_entry
            }
            
            # Save to Firebase under a different node
            url = f"{self.database_url.rstrip('/')}/processed_searches.json"
            response = requests.post(url, json=processing_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                processing_record_id = result.get("name", "unknown")
                print(f"✅ Processing result saved with ID: {processing_record_id}")
            else:
                print(f"⚠️ Could not save processing result: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Error saving processing result: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current listener status"""
        return {
            "is_running": self.is_running,
            "processed_records_count": len(self.processed_records),
            "last_processed_timestamp": self.last_processed_timestamp,
            "database_url": self.database_url
        }


# Global listener instance
_firebase_listener = None

def start_firebase_listener(poll_interval: int = 5) -> FirebaseListener:
    """
    Start the global Firebase listener
    
    Args:
        poll_interval: Seconds between polling Firebase (default: 5)
    
    Returns:
        FirebaseListener instance
    """
    global _firebase_listener
    
    if _firebase_listener is None:
        _firebase_listener = FirebaseListener()
    
    _firebase_listener.start_listening(poll_interval)
    return _firebase_listener

def stop_firebase_listener():
    """Stop the global Firebase listener"""
    global _firebase_listener
    
    if _firebase_listener:
        _firebase_listener.stop_listening()

def get_firebase_listener() -> Optional[FirebaseListener]:
    """Get the current Firebase listener instance"""
    return _firebase_listener


def main():
    """Test the Firebase listener"""
    print("🔥 Testing Firebase Listener")
    print("=" * 40)
    
    try:
        # Start listener
        listener = start_firebase_listener(poll_interval=3)
        
        # Let it run for a bit
        print("Running listener for 30 seconds...")
        print("Add some flight searches through your UI to test!")
        time.sleep(30)
        
        # Show status
        status = listener.get_status()
        print(f"\nStatus: {json.dumps(status, indent=2)}")
        
        # Stop listener
        stop_firebase_listener()
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        stop_firebase_listener()
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
