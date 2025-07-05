#!/usr/bin/env python3
"""
Quick test for async price monitoring functionality
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agent.langchain_notifier import load_prices, send_notification

async def test_async_functions():
    """Test the async functions work correctly."""
    print("🧪 Testing async price monitoring functions...")
    
    # Test loading prices
    print("1. Testing async price loading...")
    prices = await load_prices()
    print(f"   ✅ Loaded {len(prices)} price entries")
    
    # Test notification function
    if prices:
        print("2. Testing async notification...")
        test_flight = prices[0]
        notification = await send_notification(test_flight)
        print(f"   ✅ Notification sent: {notification[:50]}...")
    else:
        print("2. Skipping notification test (no prices found)")
    
    print("🎉 All async tests completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_async_functions()) 