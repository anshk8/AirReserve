#!/usr/bin/env python3
"""
Test script to trigger Discord notifications and verify they appear in Discord channel
"""

import sys
import os
import asyncio
import json
import requests
from datetime import datetime

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agent.real_time_data_manager import RealTimeDataManager

class DiscordNotificationTester:
    """Test class to trigger Discord notifications"""
    
    def __init__(self):
        self.notifications_sent = []
        self.price_drops_detected = 0
        
    async def test_discord_notification_callback(self, flight_data):
        """Callback function to test Discord notifications"""
        print(f"🔔 Discord notification callback triggered with {len(flight_data)} flights")
        
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

async def test_discord_notifications():
    """Test Discord notifications specifically"""
    
    print("🚀 Testing Discord Notifications")
    print("=" * 50)
    print("📢 This test will send actual notifications to your Discord channel!")
    print("=" * 50)
    
    # Initialize the data manager
    data_manager = RealTimeDataManager(data_dir="data", refresh_interval=30)  # Shorter interval for testing
    notification_tester = DiscordNotificationTester()
    
    print("\n📋 Test 1: Loading flight data and triggering notifications")
    print("-" * 50)
    
    try:
        # Get all flight data
        all_flights = await data_manager.get_all_flight_data()
        print(f"✅ Loaded {len(all_flights)} flights from data files")
        
        if all_flights:
            # Show what we found
            print("\n📊 Flight data found:")
            for i, flight in enumerate(all_flights[:5], 1):  # Show first 5
                price = flight.get('price', 'Unknown')
                airline = flight.get('airline', 'Unknown')
                print(f"   {i}. ${price} - {airline}")
            
            # Trigger notification callback with the data
            print(f"\n🔔 Triggering notification callback...")
            await notification_tester.test_discord_notification_callback(all_flights)
            
            print(f"\n📊 Notification Summary:")
            print(f"   📊 Price drops detected: {notification_tester.price_drops_detected}")
            print(f"   🔔 Discord notifications sent: {len(notification_tester.notifications_sent)}")
            
            if notification_tester.notifications_sent:
                print(f"\n📝 Recent notifications:")
                for notif in notification_tester.notifications_sent[-3:]:  # Show last 3
                    flight = notif['flight']
                    print(f"      ${flight.get('price')} - {flight.get('airline', 'Unknown')}")
        else:
            print("⚠️  No flight data found. Creating test data...")
            
            # Create some test data to trigger notifications
            test_flights = [
                {"price": 150, "airline": "Test Air", "departure": "Toronto", "destination": "Vancouver", "timestamp": datetime.now().isoformat()},
                {"price": 180, "airline": "Test Air", "departure": "Montreal", "destination": "Calgary", "timestamp": datetime.now().isoformat()},
                {"price": 120, "airline": "Test Air", "departure": "Ottawa", "destination": "Edmonton", "timestamp": datetime.now().isoformat()}
            ]
            
            print("🔔 Triggering notification callback with test data...")
            await notification_tester.test_discord_notification_callback(test_flights)
    
    except Exception as e:
        print(f"❌ Error in Discord notification test: {e}")
        return False
    
    print("\n📋 Test 2: Manual Discord webhook test")
    print("-" * 50)
    
    try:
        # Test Discord webhook directly
        config_path = "config/notification_config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            webhook_url = config.get('discord_webhook_url', '')
            if webhook_url and webhook_url != 'your_discord_webhook_url_here':
                print("🔗 Testing Discord webhook directly...")
                
                # Send a test message
                test_payload = {
                    "content": "🧪 **TEST MESSAGE** - This is a test notification from AirReserve LangChain Agent!",
                    "embeds": [{
                        "title": "🧪 Test Notification",
                        "description": "If you see this message, your Discord webhook is working correctly!",
                        "color": 0x00FF00,  # Green color
                        "timestamp": datetime.now().isoformat()
                    }]
                }
                
                response = requests.post(webhook_url, json=test_payload, timeout=10)
                
                if response.status_code == 204:
                    print("✅ Test Discord message sent successfully!")
                    print("📱 Check your Discord channel for the test message")
                else:
                    print(f"❌ Test Discord message failed: {response.status_code} - {response.text}")
            else:
                print("⚠️  Discord webhook not configured in config file")
        else:
            print("❌ Notification config file not found")
    
    except Exception as e:
        print(f"❌ Error in manual Discord test: {e}")
    
    return True

async def main():
    """Main test function"""
    
    print("Starting Discord Notification Tests...")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run Discord notification tests
    success = await test_discord_notifications()
    
    print("\n" + "=" * 50)
    print("📊 DISCORD NOTIFICATION TEST SUMMARY")
    print("=" * 50)
    
    if success:
        print("🎉 Discord notification tests completed!")
        print("📱 Check your Discord channel for notifications")
        print("✅ If you see messages, your webhook is working correctly")
    else:
        print("⚠️  Some Discord notification tests failed")
        print("🔧 Please check your webhook configuration")
    
    print(f"\n🏁 All tests completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main()) 