import aiohttp
import json
import ssl
import certifi
from typing import Dict, Optional

class DiscordNotifier:
    """Handles sending notifications to Discord via webhook."""
    
    def __init__(self, webhook_url: str):
        """
        Initialize Discord notifier with webhook URL.
        
        Args:
            webhook_url (str): Discord webhook URL
        """
        self.webhook_url = webhook_url
        
    async def send_notification(self, flight: Dict) -> bool:
        """
        Send a notification about a flight price drop to Discord.
        
        Args:
            flight (Dict): Flight information dictionary
            
        Returns:
            bool: True if notification was sent successfully, False otherwise
        """
        if not self.webhook_url:
            print("⚠️  No Discord webhook URL configured")
            return False
            
        try:
            # Create SSL context with certifi
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            
            # Create Discord embed
            embed = {
                "title": "🎉 Flight Price Drop Alert!",
                "color": 0x00ff00,  # Green color
                "fields": [
                    {
                        "name": "Airline",
                        "value": flight.get("airline", "Unknown"),
                        "inline": True
                    },
                    {
                        "name": "Destination",
                        "value": flight.get("destination", "Unknown"),
                        "inline": True
                    },
                    {
                        "name": "Price",
                        "value": f"${flight.get('price', 'N/A')}",
                        "inline": True
                    }
                ],
                "timestamp": flight.get("timestamp", "")
            }
            
            # Prepare Discord message
            message = {
                "embeds": [embed],
                "content": "🚨 **Price Drop Alert!** 🚨"
            }
            
            # Create connector with SSL context
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            
            # Send to Discord
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(
                    self.webhook_url,
                    json=message,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 204:
                        print(f"✅ Discord notification sent for {flight.get('airline', 'Unknown')} to {flight.get('destination', 'Unknown')}")
                        return True
                    else:
                        print(f"❌ Failed to send Discord notification: {response.status}")
                        return False
                        
        except Exception as e:
            print(f"❌ Error sending Discord notification: {e}")
            return False 