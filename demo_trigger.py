#!/usr/bin/env python3
"""
Demo Trigger Script for Live Demonstrations
Use this during your hackathon presentation to trigger live notifications!
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Add the tools directory to path
sys.path.append(str(Path(__file__).parent / "src" / "agent" / "tools"))

from langchain_notifier import send_notification, THRESHOLD

class DemoTrigger:
    """Demo trigger for live presentations"""
    
    def __init__(self):
        self.notifications_sent = 0
        
    def print_demo_trigger_header(self):
        """Print demo trigger header"""
        print("=" * 60)
        print("🎬 AIRRESERVE LIVE DEMO TRIGGER")
        print("=" * 60)
        print("Use this during your presentation to trigger live notifications!")
        print("=" * 60)
    
    async def trigger_price_drop_notification(self, airline="Demo Airlines", destination="Demo City", price=150):
        """Trigger a price drop notification for demo"""
        print(f"\n🚨 TRIGGERING PRICE DROP NOTIFICATION!")
        print(f"   Airline: {airline}")
        print(f"   Destination: {destination}")
        print(f"   Price: ${price} (below ${THRESHOLD} threshold)")
        
        demo_flight = {
            "price": price,
            "airline": airline,
            "destination": destination,
            "timestamp": datetime.now().isoformat(),
            "source": "Live Demo"
        }
        
        result = await send_notification(demo_flight)
        
        if result:
            self.notifications_sent += 1
            print(f"   ✅ Notification sent successfully!")
            print(f"   📱 Check Discord for the notification!")
            print(f"   📊 Total notifications sent: {self.notifications_sent}")
        else:
            print(f"   ⏸️  Notification throttled (wait 30 seconds)")
        
        return result
    
    async def trigger_multiple_notifications(self):
        """Trigger multiple notifications for demo"""
        print(f"\n🎬 TRIGGERING MULTIPLE NOTIFICATIONS FOR DEMO!")
        
        demo_flights = [
            {"airline": "Air Canada", "destination": "Vancouver", "price": 180},
            {"airline": "WestJet", "destination": "Toronto", "price": 160},
            {"airline": "Porter Airlines", "destination": "Montreal", "price": 140},
            {"airline": "Flair Airlines", "destination": "Calgary", "price": 120}
        ]
        
        for i, flight in enumerate(demo_flights, 1):
            print(f"\n   📤 Triggering notification {i}/4...")
            await self.trigger_price_drop_notification(
                flight["airline"], 
                flight["destination"], 
                flight["price"]
            )
            
            # Wait 2 seconds between notifications
            if i < len(demo_flights):
                print("   ⏳ Waiting 2 seconds...")
                await asyncio.sleep(2)
        
        print(f"\n🎉 Demo complete! Sent {self.notifications_sent} notifications!")
    
    def show_demo_commands(self):
        """Show demo commands for presentation"""
        print(f"\n📋 DEMO COMMANDS FOR PRESENTATION:")
        print("=" * 60)
        print("1. Start UI: npm run dev")
        print("2. Show notifications: python test_notifications.py")
        print("3. Trigger live demo: python demo_trigger.py")
        print("4. Force notification: python force_notification.py")
        print("5. Clear history: python clear_history.py")
        print("=" * 60)
    
    def show_presentation_tips(self):
        """Show presentation tips"""
        print(f"\n💡 PRESENTATION TIPS:")
        print("=" * 60)
        print("• Start with UI demo first (most visual impact)")
        print("• Show real data files to prove Tavily integration")
        print("• Trigger live notifications during presentation")
        print("• Have Discord visible on screen")
        print("• Emphasize the 24/7 monitoring aspect")
        print("• Show the beautiful Windsurf UI animations")
        print("• Demonstrate the booking simulation")
        print("• Keep backup terminal windows ready")
        print("=" * 60)

async def main():
    """Main demo trigger function"""
    trigger = DemoTrigger()
    
    # Print header
    trigger.print_demo_trigger_header()
    
    # Show demo commands
    trigger.show_demo_commands()
    
    # Show presentation tips
    trigger.show_presentation_tips()
    
    print(f"\n🎯 READY FOR LIVE DEMO!")
    print("Run this script during your presentation to trigger live notifications!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 