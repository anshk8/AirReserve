"""
Start Firebase Monitoring Service
Simple script to start monitoring Firebase for new flight searches
"""

import sys
import os
import time
from pathlib import Path

# Add the parent directory to sys.path so we can import our modules
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

try:
    from src.agent.firebase_listener import start_firebase_listener, stop_firebase_listener
    print("✅ Successfully imported Firebase listener")
except ImportError as e:
    print(f"❌ Error importing Firebase listener: {e}")
    print("Make sure you're running this from the correct directory")
    sys.exit(1)

def main():
    """Start the Firebase monitoring service"""
    print("🔥 AirReserve Firebase Monitoring Service")
    print("=" * 50)
    print("This service monitors Firebase for new flight searches")
    print("and automatically calls Tavily API when new entries are detected.")
    print("=" * 50)
    
    # Get poll interval from command line or use default
    poll_interval = 5
    if len(sys.argv) > 1:
        try:
            poll_interval = int(sys.argv[1])
        except ValueError:
            print("⚠️ Invalid poll interval provided. Using default of 5 seconds.")
    
    print(f"📡 Starting monitoring (checking every {poll_interval} seconds)")
    print("💡 Tip: Add flight searches through your UI to see the system in action!")
    print("🛑 Press Ctrl+C to stop the service")
    print()
    
    try:
        # Start the listener
        listener = start_firebase_listener(poll_interval)
        
        # Keep the service running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping service...")
        stop_firebase_listener()
        print("✅ Service stopped successfully")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        stop_firebase_listener()
        sys.exit(1)

if __name__ == "__main__":
    main()
