"""
Simple MCP Server with LangChain Integration using FastMCP
This is much easier to work with than the low-level MCP protocol
"""

import os
import json
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

# LangChain imports
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

from .tools.travelTools import search_destinations
from .tools.databaseTools import (
    save_flight_search, 
    get_flight_searches
)
from .tools.simple_tools import (
    save_flight_search_simple,
    get_flight_searches_simple, 
    search_flight_prices_simple
)
from .firebase_listener import (
    start_firebase_listener, 
    stop_firebase_listener, 
    get_firebase_listener
)
from .SYSTEMPROMPT import system_prompt

# Load environment variables
load_dotenv()

# Create FastMCP server
mcp = FastMCP("Travel Assistant MCP Server")

# Initialize LangChain components
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not set. Some features may not work.")
    llm = None
    agent = None
else:
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model="gpt-3.5-turbo",
        temperature=0
    )


# Initialize LangChain agent with tools
if llm:

    # Memory important so we can ask follow ups
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    #tools are imports from tools/ folder
    langchain_tools = [
        search_destinations,
        save_flight_search_simple,
        get_flight_searches_simple,
        search_flight_prices_simple
    ]

    

    agent = initialize_agent(
        tools=langchain_tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        handle_parsing_errors=True,
        agent_kwargs={"prefix": system_prompt}
    )
else:
    memory = None



@mcp.tool()
def find_destinations(query: str = "", budget: float = 2000.0) -> str:
    """Search for travel destinations within budget.
    
    Args:
        query: Search query for destinations (optional)
        budget: Maximum budget in USD (default: 2000)
    
    Returns:
        List of destinations within budget
    """
    input_str = f"{query},{budget}" if query else str(budget)
    return search_destinations(input_str)

@mcp.tool()
def chat_with_travel_agent(message: str) -> str:
    """Chat with the AI travel agent using LangChain.
    
    Args:
        message: Your message or question for the travel agent
    
    Returns:
        Response from the AI travel agent
    """
    if not agent:
        return "Error: OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
    
    try:
        response = agent.invoke({"input": message})
        return response.get("output", "No response from agent")
    except Exception as e:
        return f"Error from travel agent: {str(e)}"

@mcp.tool()
def plan_trip(destination: str, budget: float, duration: str = "1 week") -> str:
    """Plan a complete trip using the AI agent.
    
    Args:
        destination: Where you want to go
        budget: Your total budget in USD
        duration: How long you want to stay (default: 1 week)
    
    Returns:
        A complete trip plan
    """
    if not agent:
        return "Error: OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
    
    try:
        prompt = f"""
        Plan a {duration} trip to {destination} with a budget of ${budget}.
        Include:
        1. Flight estimates
        2. Accommodation suggestions  
        3. Daily activities
        4. Food recommendations
        5. Total cost breakdown
        6. Weather information
        
        Use the available tools to get weather and destination information.
        """
        
        response = agent.invoke({"input": prompt})
        return response.get("output", "Could not generate trip plan")
    except Exception as e:
        return f"Error planning trip: {str(e)}"


# MCP Tool Definitions for Firebase operations
@mcp.tool()
def store_flight_search(to_destination: str, from_origin: str, max_price: int, user_id: str = "default") -> str:
    """Store flight search parameters in Firebase database.
    
    Args:
        to_destination: Destination airport code or city name
        from_origin: Origin airport code or city name  
        max_price: Maximum price budget for the flight
        user_id: User identifier (optional, defaults to 'default')
    
    Returns:
        Success message with document ID or error message
    """
    return save_flight_search(to_destination, from_origin, max_price, user_id)

@mcp.tool()
def retrieve_flight_searches(user_id: str = "default", limit: int = 10) -> str:
    """Retrieve recent flight searches from Firebase database.
    
    Args:
        user_id: User identifier to filter searches
        limit: Maximum number of searches to return
    
    Returns:
        JSON string of flight searches or error message
    """
    return get_flight_searches(user_id, limit)

@mcp.tool()
def start_monitoring_firebase(poll_interval: int = 5) -> str:
    """Start monitoring Firebase for new flight search entries.
    
    Args:
        poll_interval: Seconds between checking Firebase for new entries (default: 5)
    
    Returns:
        Status message about the monitoring service
    """
    try:
        if not agent:
            return "❌ Cannot start monitoring: LangChain agent not initialized. Please check OPENAI_API_KEY."
        
        listener = start_firebase_listener(agent=agent, poll_interval=poll_interval)
        return f"✅ Firebase monitoring started with LangChain agent! Checking for new flight searches every {poll_interval} seconds. When new entries are detected, the agent will search for flights using natural language prompts."
    except Exception as e:
        return f"❌ Error starting Firebase monitoring: {str(e)}"

@mcp.tool()
def stop_monitoring_firebase() -> str:
    """Stop monitoring Firebase for new flight search entries.
    
    Returns:
        Status message about stopping the monitoring service
    """
    try:
        stop_firebase_listener()
        return "✅ Firebase monitoring stopped successfully."
    except Exception as e:
        return f"❌ Error stopping Firebase monitoring: {str(e)}"

@mcp.tool()
def get_monitoring_status() -> str:
    """Get the current status of Firebase monitoring.
    
    Returns:
        JSON string with monitoring status information
    """
    try:
        listener = get_firebase_listener()
        if listener:
            status = listener.get_status()
            return json.dumps(status, indent=2)
        else:
            return json.dumps({"is_running": False, "message": "No listener initialized"}, indent=2)
    except Exception as e:
        return f"❌ Error getting monitoring status: {str(e)}"

@mcp.tool()
def search_flight_prices(from_city: str, to_city: str, max_price: str) -> str:
    """Search for flight prices using the LangChain agent with Tavily tools.
    
    Args:
        from_city: Origin city name
        to_city: Destination city name
        max_price: Maximum price threshold as string
    
    Returns:
        Flight price information from the LangChain agent
    """
    if not agent:
        return "❌ Cannot search flights: LangChain agent not initialized. Please check OPENAI_API_KEY."
    
    try:
        prompt = f"Get me flights from {from_city} to {to_city} under ${max_price}"
        response = agent.invoke({"input": prompt})
        return response.get("output", "No response from agent")
    except Exception as e:
        return f"❌ Error from LangChain agent: {str(e)}"
if __name__ == "__main__":
    # Run the server
    mcp.run()
