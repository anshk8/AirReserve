#!/usr/bin/env python3
"""
Tavily-Integrated LangChain Agent for Flight Price Monitoring
This agent combines LangChain's conversational AI with Tavily's web crawling
to provide intelligent flight price monitoring with CLI interface.
"""

import asyncio
import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import argparse

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

# Import our custom tools
from agent.tools.tavily_price_tracker import tavily_price_tracker
from agent.real_time_data_manager import RealTimeDataManager

# Load environment variables
load_dotenv()

class TavilyLangChainAgent:
    """
    Advanced LangChain agent that uses Tavily web crawling for intelligent
    flight price monitoring with conversational interface.
    """
    
    def __init__(self, openai_api_key: str = None, tavily_api_key: str = None):
        """Initialize the agent with API keys and components."""
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.tavily_api_key = tavily_api_key or os.getenv("TAVILY_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        if not self.tavily_api_key:
            raise ValueError("Tavily API key is required")
        
        # Initialize components
        self.data_manager = RealTimeDataManager(data_dir="data", refresh_interval=300)
        self.llm = ChatOpenAI(
            api_key=self.openai_api_key,
            model="gpt-3.5-turbo",
            temperature=0.1
        )
        
        # Initialize agent
        self.agent_executor = None
        self._setup_agent()
        
        # Monitoring state
        self.is_monitoring = False
        self.monitoring_task = None
        self.current_routes = []
        
    def _setup_agent(self):
        """Set up the LangChain agent with tools and prompts."""
        
        # Define the system prompt
        system_prompt = """You are an intelligent flight price monitoring assistant powered by Tavily web crawling.

Your capabilities:
1. Search for flight prices using real-time web data via Tavily API
2. Monitor multiple flight routes simultaneously
3. Set price alerts and thresholds
4. Provide detailed price analysis and recommendations
5. Save and manage flight data locally

When users ask about flights, always:
- Use the tavily_search_flights tool to get current prices
- Provide clear, actionable information
- Suggest price thresholds based on market data
- Offer to set up monitoring for good deals

Be helpful, accurate, and proactive in suggesting money-saving opportunities."""

        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Create agent with tools
        tools = [
            tavily_search_flights,
            start_flight_monitoring,
            stop_flight_monitoring,
            get_saved_flight_data,
            analyze_price_trends,
            set_price_alert
        ]
        
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt
        )
        
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            return_intermediate_steps=True,
            max_iterations=5
        )
    
    async def chat(self, message: str, chat_history: List = None) -> str:
        """Process a chat message and return the agent's response."""
        if not chat_history:
            chat_history = []
        
        try:
            response = await self.agent_executor.ainvoke({
                "input": message,
                "chat_history": chat_history
            })
            return response["output"]
        except Exception as e:
            return f"I encountered an error: {str(e)}. Please try rephrasing your request."
    
    async def start_cli(self):
        """Start the interactive CLI interface."""
        print("🤖 Tavily-LangChain Flight Price Agent")
        print("=" * 50)
        print("I can help you find and monitor flight prices using real-time web data!")
        print("Type 'help' for commands, 'quit' to exit.")
        print()
        
        chat_history = []
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye! Safe travels!")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if not user_input:
                    continue
                
                print("🤖 Agent: ", end="", flush=True)
                response = await self.chat(user_input, chat_history)
                print(response)
                
                # Update chat history
                chat_history.append(HumanMessage(content=user_input))
                chat_history.append({"role": "assistant", "content": response})
                
                # Keep history manageable
                if len(chat_history) > 10:
                    chat_history = chat_history[-8:]
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Safe travels!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _show_help(self):
        """Show help information."""
        help_text = """
🆘 Available Commands and Examples:

Flight Search:
• "Find flights from Toronto to Vancouver under $500"
• "What are the cheapest flights from NYC to LA?"
• "Search for flights from Montreal to Calgary"

Price Monitoring:
• "Monitor flights from Toronto to Ottawa, alert me if under $300"
• "Start monitoring Vancouver to Toronto flights"
• "Stop monitoring all flights"

Data Analysis:
• "Show me saved flight data"
• "Analyze price trends for Toronto to Vancouver"
• "What's the best time to book flights to Europe?"

General:
• Type 'quit' or 'exit' to leave
• Be specific about cities and price ranges for best results
• I'll use real-time web data to find current prices
        """
        print(help_text)

# LangChain Tools for the Agent

@tool
async def tavily_search_flights(from_city: str, to_city: str, max_price: str = "1000") -> str:
    """
    Search for flight prices using Tavily web crawling.
    
    Args:
        from_city: Origin city
        to_city: Destination city  
        max_price: Maximum price threshold (default: 1000)
    
    Returns:
        Formatted flight price information
    """
    try:
        result = tavily_price_tracker.invoke({
            "from_city": from_city,
            "to_city": to_city,
            "max_price": max_price
        })
        return result
    except Exception as e:
        return f"Error searching flights: {str(e)}"

@tool
async def start_flight_monitoring(from_city: str, to_city: str, threshold: str = "500") -> str:
    """
    Start monitoring a flight route for price drops.
    
    Args:
        from_city: Origin city
        to_city: Destination city
        threshold: Price threshold for alerts
    
    Returns:
        Confirmation message
    """
    try:
        # First get current prices
        current_result = await tavily_search_flights(from_city, to_city, threshold)
        
        # Save monitoring configuration
        config = {
            "route": f"{from_city} to {to_city}",
            "threshold": int(threshold),
            "started_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        # Save to monitoring config file
        config_dir = Path("data/monitoring")
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config_file = config_dir / f"monitor_{from_city}_{to_city}.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        return f"✅ Started monitoring {from_city} to {to_city} flights. Will alert when prices drop below ${threshold}.\n\nCurrent status:\n{current_result}"
        
    except Exception as e:
        return f"Error starting monitoring: {str(e)}"

@tool
async def stop_flight_monitoring(from_city: str = "", to_city: str = "") -> str:
    """
    Stop monitoring flight routes.
    
    Args:
        from_city: Origin city (empty to stop all)
        to_city: Destination city (empty to stop all)
    
    Returns:
        Confirmation message
    """
    try:
        config_dir = Path("data/monitoring")
        if not config_dir.exists():
            return "No active monitoring found."
        
        if from_city and to_city:
            # Stop specific route
            config_file = config_dir / f"monitor_{from_city}_{to_city}.json"
            if config_file.exists():
                config_file.unlink()
                return f"✅ Stopped monitoring {from_city} to {to_city} flights."
            else:
                return f"No monitoring found for {from_city} to {to_city}."
        else:
            # Stop all monitoring
            count = 0
            for config_file in config_dir.glob("monitor_*.json"):
                config_file.unlink()
                count += 1
            
            if count > 0:
                return f"✅ Stopped monitoring {count} flight route(s)."
            else:
                return "No active monitoring found."
                
    except Exception as e:
        return f"Error stopping monitoring: {str(e)}"

@tool
async def get_saved_flight_data(from_city: str = "", to_city: str = "") -> str:
    """
    Get saved flight data from previous searches.
    
    Args:
        from_city: Origin city (empty for all)
        to_city: Destination city (empty for all)
    
    Returns:
        Formatted flight data summary
    """
    try:
        data_dir = Path("data")
        if not data_dir.exists():
            return "No saved flight data found."
        
        if from_city and to_city:
            # Get specific route data
            data_file = data_dir / f"flight_prices_{from_city}_{to_city}.json"
            if not data_file.exists():
                return f"No saved data found for {from_city} to {to_city}."
            
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            if not data.get("searches"):
                return f"No flight searches found for {from_city} to {to_city}."
            
            latest_search = data["searches"][-1]
            flights = latest_search.get("flights", [])
            
            if not flights:
                return f"No flights found in latest search for {from_city} to {to_city}."
            
            result = f"📊 Latest data for {from_city} to {to_city}:\n"
            result += f"🕒 Last updated: {latest_search.get('search_timestamp', 'Unknown')}\n"
            result += f"✈️ Flights found: {len(flights)}\n\n"
            
            for i, flight in enumerate(flights[:5], 1):
                price = flight.get('price', 'N/A')
                airline = flight.get('airline', 'Unknown')
                result += f"{i}. ${price} - {airline}\n"
            
            return result
        else:
            # Get all saved data summary
            flight_files = list(data_dir.glob("flight_prices_*.json"))
            if not flight_files:
                return "No saved flight data found."
            
            result = f"📊 Saved Flight Data Summary ({len(flight_files)} routes):\n\n"
            
            for file_path in flight_files[:10]:  # Show up to 10 routes
                try:
                    filename = file_path.stem
                    route = filename.replace("flight_prices_", "").replace("_", " to ")
                    
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    
                    if data.get("searches"):
                        latest_search = data["searches"][-1]
                        flight_count = len(latest_search.get("flights", []))
                        timestamp = latest_search.get("search_timestamp", "Unknown")
                        result += f"• {route}: {flight_count} flights (updated: {timestamp[:10]})\n"
                    
                except Exception as e:
                    result += f"• {route}: Error reading data\n"
            
            return result
            
    except Exception as e:
        return f"Error retrieving flight data: {str(e)}"

@tool
async def analyze_price_trends(from_city: str, to_city: str) -> str:
    """
    Analyze price trends for a specific route.
    
    Args:
        from_city: Origin city
        to_city: Destination city
    
    Returns:
        Price trend analysis
    """
    try:
        data_file = Path(f"data/flight_prices_{from_city}_{to_city}.json")
        if not data_file.exists():
            return f"No historical data found for {from_city} to {to_city}. Search for flights first to build price history."
        
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        searches = data.get("searches", [])
        if len(searches) < 2:
            return f"Need more historical data for trend analysis. Only {len(searches)} search(es) found."
        
        # Analyze trends
        prices = []
        dates = []
        
        for search in searches:
            flights = search.get("flights", [])
            if flights:
                # Get average price for this search
                valid_prices = [float(f.get("price", 0)) for f in flights if f.get("price")]
                if valid_prices:
                    avg_price = sum(valid_prices) / len(valid_prices)
                    prices.append(avg_price)
                    dates.append(search.get("search_timestamp", ""))
        
        if len(prices) < 2:
            return "Insufficient price data for trend analysis."
        
        # Calculate trend
        recent_avg = sum(prices[-3:]) / len(prices[-3:]) if len(prices) >= 3 else prices[-1]
        older_avg = sum(prices[:-3]) / len(prices[:-3]) if len(prices) > 3 else prices[0]
        
        trend = "stable"
        if recent_avg < older_avg * 0.9:
            trend = "decreasing"
        elif recent_avg > older_avg * 1.1:
            trend = "increasing"
        
        min_price = min(prices)
        max_price = max(prices)
        current_price = prices[-1]
        
        result = f"📈 Price Trend Analysis for {from_city} to {to_city}:\n\n"
        result += f"📊 Data points: {len(prices)} searches\n"
        result += f"💰 Current average: ${current_price:.2f}\n"
        result += f"📉 Lowest seen: ${min_price:.2f}\n"
        result += f"📈 Highest seen: ${max_price:.2f}\n"
        result += f"📊 Trend: {trend.upper()}\n\n"
        
        if trend == "decreasing":
            result += "🎉 Great news! Prices are trending down. This might be a good time to book!"
        elif trend == "increasing":
            result += "⚠️ Prices are trending up. Consider booking soon or setting a price alert."
        else:
            result += "📊 Prices are relatively stable. Monitor for sudden drops."
        
        return result
        
    except Exception as e:
        return f"Error analyzing price trends: {str(e)}"

@tool
async def set_price_alert(from_city: str, to_city: str, target_price: str) -> str:
    """
    Set a price alert for a specific route.
    
    Args:
        from_city: Origin city
        to_city: Destination city
        target_price: Target price for alert
    
    Returns:
        Confirmation message
    """
    try:
        target = float(target_price)
        
        # Create alert configuration
        alert_config = {
            "route": f"{from_city} to {to_city}",
            "target_price": target,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "notifications_sent": 0
        }
        
        # Save alert
        alerts_dir = Path("data/alerts")
        alerts_dir.mkdir(parents=True, exist_ok=True)
        
        alert_file = alerts_dir / f"alert_{from_city}_{to_city}_{target}.json"
        with open(alert_file, 'w') as f:
            json.dump(alert_config, f, indent=2)
        
        # Get current prices to compare
        current_result = await tavily_search_flights(from_city, to_city, str(int(target * 1.5)))
        
        result = f"🔔 Price alert set for {from_city} to {to_city} at ${target}!\n\n"
        result += f"I'll notify you when flights drop to ${target} or below.\n\n"
        result += f"Current market status:\n{current_result}"
        
        return result
        
    except ValueError:
        return f"Invalid price format: {target_price}. Please enter a number."
    except Exception as e:
        return f"Error setting price alert: {str(e)}"

async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Tavily-LangChain Flight Price Agent")
    parser.add_argument("--openai-key", help="OpenAI API key")
    parser.add_argument("--tavily-key", help="Tavily API key")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    
    args = parser.parse_args()
    
    try:
        # Initialize agent
        agent = TavilyLangChainAgent(
            openai_api_key=args.openai_key,
            tavily_api_key=args.tavily_key
        )
        
        if args.test:
            # Test mode - run some sample queries
            print("🧪 Running in test mode...")
            
            test_queries = [
                "Find flights from Toronto to Vancouver under $600",
                "What are the cheapest flights from Montreal to Calgary?",
                "Show me saved flight data"
            ]
            
            for query in test_queries:
                print(f"\n🧪 Test Query: {query}")
                response = await agent.chat(query)
                print(f"🤖 Response: {response}")
        else:
            # Interactive CLI mode
            await agent.start_cli()
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please set your API keys in .env file or pass them as arguments.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
