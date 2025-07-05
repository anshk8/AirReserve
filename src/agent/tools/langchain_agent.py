#!/usr/bin/env python3
"""
LangChain Agent for Asynchronous Price Monitoring
This module integrates the async price monitoring with LangChain's agent framework.
"""

import asyncio
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_notifier import monitor_prices, load_prices, send_notification

class PriceMonitoringAgent:
    """LangChain agent for monitoring flight prices asynchronously."""
    
    def __init__(self, threshold=200, check_interval=60):
        self.threshold = threshold
        self.check_interval = check_interval
        self.monitoring_task = None
        self.is_monitoring = False
        
    async def start_monitoring(self):
        """Start the async price monitoring in the background."""
        if self.is_monitoring:
            print("⚠️  Monitoring is already running")
            return
            
        self.is_monitoring = True
        self.monitoring_task = asyncio.create_task(
            monitor_prices(self.threshold, self.check_interval)
        )
        print(f"✅ Started async price monitoring (threshold: ${self.threshold})")
        
    async def stop_monitoring(self):
        """Stop the async price monitoring."""
        if not self.is_monitoring:
            print("⚠️  Monitoring is not running")
            return
            
        self.is_monitoring = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        print("🛑 Stopped price monitoring")
        
    async def get_current_prices(self):
        """Get current flight prices."""
        return await load_prices()
        
    async def check_price_drops(self):
        """Check for price drops and return notifications."""
        prices = await load_prices()
        notifications = []
        
        for flight in prices:
            try:
                price = float(flight.get("price", float('inf')))
                if price < self.threshold:
                    notification = await send_notification(flight)
                    notifications.append(notification)
            except Exception as e:
                print(f"❌ Error checking flight: {e}")
                
        return notifications

# LangChain tools for the agent
@tool
async def start_price_monitoring(threshold: int = 200) -> str:
    """Start monitoring flight prices for drops below the specified threshold."""
    agent = PriceMonitoringAgent(threshold=threshold)
    await agent.start_monitoring()
    return f"Started monitoring with threshold ${threshold}"

@tool
async def stop_price_monitoring() -> str:
    """Stop the current price monitoring."""
    agent = PriceMonitoringAgent()
    await agent.stop_monitoring()
    return "Stopped price monitoring"

@tool
async def get_flight_prices() -> str:
    """Get current flight prices from the data file."""
    agent = PriceMonitoringAgent()
    prices = await agent.get_current_prices()
    if not prices:
        return "No flight prices found"
    
    result = "Current flight prices:\n"
    for i, flight in enumerate(prices[:5], 1):  # Show top 5
        result += f"{i}. {flight.get('airline', 'Unknown')} to {flight.get('destination', 'Unknown')}: ${flight.get('price', 'N/A')}\n"
    return result

@tool
async def check_for_price_drops(threshold: int = 200) -> str:
    """Check for any price drops below the specified threshold."""
    agent = PriceMonitoringAgent(threshold=threshold)
    notifications = await agent.check_price_drops()
    
    if not notifications:
        return f"No price drops found below ${threshold}"
    
    return f"Found {len(notifications)} price drop(s):\n" + "\n".join(notifications)

# Create LangChain agent
def create_price_monitoring_agent():
    """Create and configure the LangChain price monitoring agent."""
    
    # System message
    system_message = SystemMessage(content="""
    You are a flight price monitoring assistant. You can:
    1. Start monitoring flight prices for drops below a threshold
    2. Stop monitoring
    3. Get current flight prices
    4. Check for price drops
    
    Use the available tools to help users monitor flight prices effectively.
    """)
    
    # Tools
    tools = [
        start_price_monitoring,
        stop_price_monitoring,
        get_flight_prices,
        check_for_price_drops
    ]
    
    # Create agent (placeholder - would need OpenAI API key for full implementation)
    # For now, we'll create a basic structure
    return {
        "system_message": system_message,
        "tools": tools,
        "description": "Flight price monitoring agent with async capabilities"
    }

async def main():
    """Main function to run the LangChain agent."""
    print("🤖 Starting LangChain Price Monitoring Agent...")
    
    # Create agent
    agent_config = create_price_monitoring_agent()
    print(f"✅ Agent created with {len(agent_config['tools'])} tools")
    
    # Example usage
    agent = PriceMonitoringAgent(threshold=200)
    
    # Start monitoring
    await agent.start_monitoring()
    
    # Keep running for a while
    try:
        await asyncio.sleep(120)  # Run for 2 minutes
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    finally:
        await agent.stop_monitoring()

if __name__ == "__main__":
    asyncio.run(main()) 