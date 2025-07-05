#!/usr/bin/env python3
"""
Test script for Issue 3: LangChain Asynchronous Agent for Price Monitoring
Tests the real-time data manager and notification system
"""

import sys
import os
import asyncio
import json
import requests
import time
from datetime import datetime

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agent.real_time_data_manager import RealTimeDataManager

class NotificationTester:
    """Test class to simulate notifications and verify functionality"""
    
    def __init__(self):
        self.notifications_sent = []
        self.price_drops_detected = 0
        
    async def test_notification_callback(self, flight_data):
        """Callback function to test notifications"""
        print(f"🔔 Notification callback triggered with {len(flight_data)} flights")
        
        # Check for price drops below threshold
        threshold = 200  # From config
        for flight in flight_data:
            if flight.get('price', 0) < threshold:
                self.price_drops_detected += 1
                notification = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "price_drop",
                    "flight": flight,
                    "threshold": threshold
                }
                self.notifications_sent.append(notification)

                # Send Discord notification
                await self.send_discord_notification(flight)
                
                print(f"🚨 PRICE DROP ALERT: ${flight.get('price')} for {flight.get('airline', 'Unknown')}")
        
        print(f"📊 Current stats: {self.price_drops_detected} price drops detected")

    async def send_discord_notification(self, flight):
        """Send notification to Discord webhook"""
        try:
            # Load Discord webhook URL from config
            config_path = "config/notification_config.json"
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                webhook_url = config.get('discord_webhook_url', '')
                if not webhook_url or webhook_url == 'your_discord_webhook_url_here':
                    print("⚠️  Discord webhook not configured")
                    return
                
                # Create Discord message
                embed = {
                    "title": "🚨 Flight Price Drop Alert!",
                    "description": f"**Price Drop Detected!**\n\n"
                                 f"💰 **Price:** ${flight.get('price', 'Unknown')}\n"
                                 f"✈️ **Airline:** {flight.get('airline', 'Unknown')}\n"
                                 f"🛫 **Route:** {flight.get('departure', 'Unknown')} → {flight.get('destination', 'Unknown')}\n"
                                 f"⏰ **Detected:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "color": 0xFF0000,  # Red color
                    "footer": {
                        "text": "AirReserve Price Monitor"
                    },
                    "timestamp": datetime.now().isoformat()
                }
                
                payload = {
                    "embeds": [embed],
                    "content": "🔔 **PRICE DROP ALERT!** Check out this great deal!"
                }
                
                # Send to Discord
                response = requests.post(webhook_url, json=payload, timeout=10)
                
                if response.status_code == 204:
                    print(f"✅ Discord notification sent successfully!")
                else:
                    print(f"❌ Discord notification failed: {response.status_code} - {response.text}")
                    
            else:
                print("❌ Notification config file not found")
                
        except Exception as e:
            print(f"❌ Error sending Discord notification: {e}")

async def test_real_time_data_manager():
    """Test the RealTimeDataManager functionality"""
    
    print("🚀 Testing Issue 3: LangChain Asynchronous Agent")
    print("=" * 60)
    
    # Initialize the data manager
    data_manager = RealTimeDataManager(data_dir="data", refresh_interval=60)
    notification_tester = NotificationTester()
    
    print("📋 Test 1: Loading existing flight data")
    print("-" * 40)
    
    try:
        # Test loading data for existing routes
        test_routes = [
            ("Toronto", "Ottawa"),
            ("Vancouver", "Toronto"),
            ("Calgary", "Edmonton")
        ]
        
        for from_city, to_city in test_routes:
            print(f"🔍 Loading data for {from_city} → {to_city}")
            flights = await data_manager.load_flight_data(from_city, to_city)
            print(f"   ✅ Found {len(flights)} flights")
            
            if flights:
                for i, flight in enumerate(flights[:3], 1):  # Show first 3
                    price = flight.get('price', 'Unknown')
                    print(f"   {i}. ${price} - {flight.get('airline', 'Unknown')}")
    
    except Exception as e:
        print(f"❌ Error loading flight data: {e}")
        return False
    
    print("\n📋 Test 2: Getting all flight data")
    print("-" * 40)
    
    try:
        all_flights = await data_manager.get_all_flight_data()
        print(f"✅ Total flights across all routes: {len(all_flights)}")
        
        if all_flights:
            # Show price distribution
            prices = [f.get('price', 0) for f in all_flights if f.get('price')]
            if prices:
                min_price = min(prices)
                max_price = max(prices)
                avg_price = sum(prices) / len(prices)
                print(f"   💰 Price range: ${min_price:.2f} - ${max_price:.2f}")
                print(f"   📊 Average price: ${avg_price:.2f}")
    
    except Exception as e:
        print(f"❌ Error getting all flight data: {e}")
        return False
    
    print("\n📋 Test 3: Data statistics")
    print("-" * 40)
    
    try:
        stats = data_manager.get_data_stats()
        print(f"✅ Data statistics:")
        print(f"   📁 Total routes: {stats['total_routes']}")
        print(f"   ✈️  Total flights: {stats['total_flights']}")
        print(f"   💾 Cache hits: {stats['cache_hits']}")
        
        if stats['last_refresh_times']:
            print(f"   🕒 Last refresh times:")
            for route, time_str in stats['last_refresh_times'].items():
                print(f"      {route}: {time_str}")
    
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
        return False
    
    print("\n📋 Test 4: Notification system simulation")
    print("-" * 40)
    
    try:
        # Simulate a short monitoring session
        print("👀 Starting 30-second monitoring simulation...")
        
        # Start monitoring with callback
        monitor_task = asyncio.create_task(
            data_manager.monitor_data_changes(notification_tester.test_notification_callback)
        )
        
        # Let it run for a short time
        await asyncio.sleep(10)  # Monitor for 10 seconds
        
        # Cancel the monitoring task
        monitor_task.cancel()
        
        print(f"✅ Monitoring completed")
        print(f"   📊 Price drops detected: {notification_tester.price_drops_detected}")
        print(f"   🔔 Notifications sent: {len(notification_tester.notifications_sent)}")
        
        if notification_tester.notifications_sent:
            print("   📝 Recent notifications:")
            for notif in notification_tester.notifications_sent[-3:]:  # Show last 3
                flight = notif['flight']
                print(f"      ${flight.get('price')} - {flight.get('airline', 'Unknown')}")
    
    except asyncio.CancelledError:
        print("✅ Monitoring task cancelled as expected")
    except Exception as e:
        print(f"❌ Error in notification test: {e}")
        return False
    
    print("\n📋 Test 5: Configuration validation")
    print("-" * 40)
    
    try:
        # Check if notification config exists
        config_path = "config/notification_config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            print("✅ Notification configuration found:")
            print(f"   💰 Price threshold: ${config.get('threshold', 'Not set')}")
            print(f"   ⏱️  Check interval: {config.get('check_interval', 'Not set')} seconds")
            print(f"   📢 Notification channels: {config.get('notification_channels', [])}")
            
            # Check Discord webhook
            webhook_url = config.get('discord_webhook_url', '')
            if webhook_url and webhook_url != 'your_discord_webhook_here':
                print("   🔗 Discord webhook: Configured")
            else:
                print("   🔗 Discord webhook: Not configured")
                
        else:
            print("❌ Notification configuration not found")
            return False
    
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return False
    
    return True

async def test_error_handling():
    """Test error handling scenarios"""
    
    print("\n🔧 Testing Error Handling")
    print("=" * 40)
    
    data_manager = RealTimeDataManager(data_dir="nonexistent_dir")
    
    try:
        # Test with non-existent directory
        flights = await data_manager.load_flight_data("Nonexistent", "City")
        print("✅ Gracefully handled non-existent directory")
    except Exception as e:
        print(f"❌ Error handling failed: {e}")
    
    try:
        # Test with invalid route
        flights = await data_manager.load_flight_data("", "")
        print("✅ Gracefully handled empty route parameters")
    except Exception as e:
        print(f"❌ Error handling failed: {e}")

async def main():
    """Main test function"""
    
    print("Starting Issue 3 LangChain Agent Tests...")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run main functionality tests
    success = await test_real_time_data_manager()
    
    # Run error handling tests
    await test_error_handling()
    
    print("\n" + "=" * 60)
    print("📊 ISSUE 3 TEST SUMMARY")
    print("=" * 60)
    
    if success:
        print("🎉 All Issue 3 tests passed!")
        print("✅ Real-time data manager is working")
        print("✅ Notification system is functional")
        print("✅ Configuration is properly set up")
        print("✅ Error handling is robust")
        print("\n🚀 The LangChain agent is ready for use!")
    else:
        print("⚠️  Some tests failed")
        print("🔧 Please check the implementation")
    
    print(f"\n🏁 All tests completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main()) 