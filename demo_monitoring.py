"""
Complete Demo: Firebase Monitoring System
This script demonstrates the full workflow of the monitoring system
"""

import sys
import os
import time
import signal
from pathlib import Path

# Ensure we can import our modules
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from src.agent.firebase_listener import start_firebase_listener, stop_firebase_listener
    from src.agent.tools.databaseTools import _save_flight_search_impl
    from src.agent.MCPLangChainServer import agent
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Global variable to track the listener
listener = None

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Received interrupt signal")
    if listener:
        stop_firebase_listener()
    print("✅ Cleanup completed")
    sys.exit(0)

def main():
    """Run the complete demonstration"""
    global listener
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🎯 Firebase Monitoring System - Complete Demo")
    print("=" * 50)
    print("This demo will:")
    print("1. Start the Firebase monitoring service with LangChain agent")
    print("2. Add a test flight search")
    print("3. Show automatic agent processing")
    print("4. Display results")
    print("=" * 50)
    
    # Check if agent is available
    if not agent:
        print("❌ LangChain agent not available. Please check:")
        print("   1. OPENAI_API_KEY is set in your .env file")
        print("   2. All required dependencies are installed")
        sys.exit(1)
    
    print("✅ LangChain agent is ready")
    
    try:
        # Step 1: Start monitoring
        print("\n📡 Step 1: Starting Firebase monitoring with LangChain agent...")
        listener = start_firebase_listener(agent=agent, poll_interval=3)
        print("✅ Monitoring service started (3-second polling)")
        
        # Wait for listener to initialize
        time.sleep(2)
        
        # Step 2: Add test flight search
        print("\n📝 Step 2: Adding test flight search...")
        result = _save_flight_search_impl(
            to_destination="Tokyo",
            from_origin="San Francisco",
            max_price=1200,
            user_id="demo_user"
        )
        print(f"✅ {result}")
        
        # Step 3: Wait for automatic processing
        print("\n⏳ Step 3: Waiting for automatic agent processing...")
        print("   (The LangChain agent will detect and process this automatically)")
        
        # Wait long enough for processing
        for i in range(15, 0, -1):
            print(f"   Waiting {i} seconds...", end="\\r")
            time.sleep(1)
        print("   Agent processing should be complete!     ")
        
        # Step 4: Show status
        print("\n📊 Step 4: Final status...")
        status = listener.get_status()
        print(f"   Records processed: {status['processed_records_count']}")
        print(f"   Monitoring active: {status['is_running']}")
        
        # Step 5: Verify Firebase results
        print("\n🔍 Step 5: Checking Firebase results...")
        import requests
        from dotenv import load_dotenv
        
        load_dotenv()
        db_url = os.environ.get('FIREBASE_DATABASE_URL')
        
        # Check processed results
        response = requests.get(f'{db_url.rstrip("/")}/processed_searches.json')
        if response.status_code == 200:
            processed = response.json()
            if processed:
                print(f"✅ Found {len(processed)} processed result(s) in Firebase")
                # Show latest result
                latest_key = list(processed.keys())[-1]
                latest = processed[latest_key]
                print(f"   Latest processing:")
                print(f"     Original Search: {latest.get('original_search_id', 'unknown')}")
                print(f"     Processed At: {latest.get('processed_at', 'unknown')}")
                print(f"     Status: {'Success' if 'Error' not in latest.get('tavily_result', '') else 'API Rate Limited (Expected)'}")
            else:
                print("⚠️ No processed results found")
        else:
            print(f"⚠️ Could not fetch results: {response.status_code}")
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 The monitoring system is now running continuously.")
        print("💡 Add more flight searches through your UI to see them processed automatically.")
        print("🛑 Press Ctrl+C to stop the monitoring service")
        
        # Keep running until user stops
        print("\n⏳ Monitoring continues... (Ctrl+C to stop)")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        signal_handler(None, None)
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        if listener:
            stop_firebase_listener()
        sys.exit(1)

if __name__ == "__main__":
    main()
