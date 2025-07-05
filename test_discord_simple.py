#!/usr/bin/env python3
"""
Simple Discord webhook test to verify connectivity
"""

import aiohttp
import asyncio
import ssl
import certifi

async def test_discord_webhook():
    """Test Discord webhook with SSL context"""
    
    webhook_url = "https://discord.com/api/webhooks/1391102467189637221/tql23WreNHxNlQ4Aaz-N3ELvWYLw4-R_S4bKHvZqmjykSxW53VKhQKjiT6K1p-44SLQr"
    
    # Create SSL context with certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    
    # Test message
    message = {
        "content": "🧪 **Test Notification** - AirReserve is working!",
        "embeds": [{
            "title": "Test Flight Alert",
            "description": "This is a test notification from AirReserve",
            "color": 0x00ff00,
            "fields": [
                {"name": "Airline", "value": "Test Airline", "inline": True},
                {"name": "Destination", "value": "Test City", "inline": True},
                {"name": "Price", "value": "$150", "inline": True}
            ]
        }]
    }
    
    try:
        print("🔗 Testing Discord webhook...")
        
        # Create connector with SSL context
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(
                webhook_url,
                json=message,
                headers={"Content-Type": "application/json"}
            ) as response:
                print(f"📡 Response status: {response.status}")
                print(f"📡 Response text: {await response.text()}")
                
                if response.status == 204:
                    print("✅ Discord notification sent successfully!")
                    return True
                else:
                    print(f"❌ Failed to send Discord notification: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Error testing Discord webhook: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Starting Discord webhook test...")
    asyncio.run(test_discord_webhook()) 