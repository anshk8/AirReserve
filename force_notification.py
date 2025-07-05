#!/usr/bin/env python3
"""
Force a fresh notification by clearing throttle cache
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the tools directory to path
sys.path.append(str(Path(__file__).parent / "src" / "agent" / "tools"))

from langchain_notifier import send_notification, THRESHOLD
from notification_manager import NotificationManager

async def force_notification():
    """Force a fresh notification by clearing throttle cache"""
    
    print(f"🧪 Forcing fresh notification with threshold: ${THRESHOLD}")
    
    # Clear the throttle cache by creating a new notification manager
    notification_manager = NotificationManager(throttle_minutes=0)  # No throttling
    
    # Create a test flight that should trigger notification
    test_flight = {
        "price": 150.0,
        "airline": "Test Airline",
        "destination": "Test Destination",
        "timestamp": "2025-07-05T15:00:00"
    }
    
    print(f"📤 Sending test notification for: {test_flight['airline']} to {test_flight['destination']} at ${test_flight['price']}")
    
    # Send notification
    result = await send_notification(test_flight)
    
    if result:
        print("✅ Test notification sent successfully!")
    else:
        print("❌ Test notification failed!")

if __name__ == "__main__":
    asyncio.run(force_notification()) 