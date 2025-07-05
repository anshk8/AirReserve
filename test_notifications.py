#!/usr/bin/env python3
"""
Test script to manually trigger notifications with existing flight data
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the tools directory to path
sys.path.append(str(Path(__file__).parent / "src" / "agent" / "tools"))

from langchain_notifier import send_notification, THRESHOLD

async def test_notifications():
    """Test notifications with existing flight data"""
    
    print(f"🧪 Testing notifications with threshold: ${THRESHOLD}")
    
    # Load flight data from the data directory
    data_dir = Path("data")
    flight_files = list(data_dir.glob("flight_prices_*.json"))
    
    print(f"📁 Found {len(flight_files)} flight data files")
    
    total_notifications = 0
    
    for file_path in flight_files:
        print(f"\n📄 Processing: {file_path.name}")
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Extract flights from the most recent search
            if data.get("searches"):
                latest_search = data["searches"][-1]
                flights = latest_search.get("flights", [])
                
                print(f"   Found {len(flights)} flights")
                
                for flight in flights:
                    price = float(flight.get("price", float('inf')))
                    airline = flight.get("airline", "Unknown")
                    destination = flight.get("destination", "Unknown")
                    
                    print(f"   Flight: {airline} to {destination} at ${price}")
                    
                    if price < THRESHOLD:
                        print(f"   🎯 Price ${price} is below threshold ${THRESHOLD} - sending notification!")
                        result = await send_notification(flight)
                        if result:
                            total_notifications += 1
                            print(f"   ✅ Notification sent!")
                        else:
                            print(f"   ⏸️  Notification throttled or failed")
                    else:
                        print(f"   ❌ Price ${price} is above threshold ${THRESHOLD}")
                        
        except Exception as e:
            print(f"   ❌ Error processing {file_path}: {e}")
    
    print(f"\n📊 Test complete! Sent {total_notifications} notifications")

if __name__ == "__main__":
    asyncio.run(test_notifications()) 