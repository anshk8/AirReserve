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
from .tools.databaseTools import _get_flight_searches_impl

# Load environment variables
load_dotenv()

class FirebaseListener:
    def __init__(self, agent=None):
        self.database_url = os.environ.get("FIREBASE_DATABASE_URL")
        self.last_processed_timestamp = None
        self.is_running = False
        self.listener_thread = None
        self.processed_records = set()  # Track processed record IDs
        self.agent = agent  # LangChain agent instance
        
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
            # Handle different field name formats
            to_destination = entry.get("TO", entry.get("to", ""))
            from_origin = entry.get("FROM", entry.get("from", ""))
            max_price_raw = entry.get("MAX_PRICE", entry.get("maxPrice", 0))
            user_id = entry.get("USER_ID", entry.get("userId", "default"))
            timestamp = entry.get("TIMESTAMP", entry.get("timestamp", ""))
            
            # Convert max_price to integer if it's a string
            try:
                max_price = int(max_price_raw) if max_price_raw else 0
            except (ValueError, TypeError):
                print(f"⚠️ Invalid max_price format: {max_price_raw}, defaulting to 0")
                max_price = 0
            
            print(f"\n🎯 Processing flight search {record_id}")
            print(f"   📍 Route: {from_origin} → {to_destination}")
            print(f"   💰 Max Price: ${max_price}")
            print(f"   👤 User: {user_id}")
            print(f"   ⏰ Created: {timestamp}")
            
            # Validate required fields
            if not all([to_destination, from_origin, max_price]):
                print(f"❌ Missing required fields in record {record_id}")
                return
            
            # Call LangChain agent with natural language prompt
            print(f"🤖 Calling LangChain agent for flight search...")
            
            if not self.agent:
                result = "❌ No LangChain agent provided to Firebase listener. Cannot process flight search."
                print(result)
            else:
                # Create natural language prompt for the agent
                prompt = f"Get me flights from {from_origin} to {to_destination} under ${max_price}"
                print(f"   Agent prompt: '{prompt}'")
                
                try:
                    # Use the LangChain agent (which has Tavily tools)
                    response = self.agent.invoke({"input": prompt})
                    result = response.get("output", "No response from agent")
                    print(f"✅ Agent response received")
                except Exception as e:
                    result = f"❌ Error from LangChain agent: {str(e)}"
                    print(result)
            
            print(f"📋 Agent Result:")
            print(f"   {result}")
            
            # Results are only logged to console, not saved to Firebase
            
        except Exception as e:
            print(f"❌ Error processing flight search {entry.get('record_id', 'unknown')}: {str(e)}")
    
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

def start_firebase_listener(agent=None, poll_interval: int = 5) -> FirebaseListener:
    """
    Start the global Firebase listener
    
    Args:
        agent: LangChain agent instance with Tavily tools
        poll_interval: Seconds between polling Firebase (default: 5)
    
    Returns:
        FirebaseListener instance
    """
    global _firebase_listener
    
    if _firebase_listener is None:
        _firebase_listener = FirebaseListener(agent=agent)
    
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
