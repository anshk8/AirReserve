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
        save_flight_search,
        get_flight_searches
    ]

    

    agent = initialize_agent(
        tools=langchain_tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
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

if __name__ == "__main__":
    # Run the server
    mcp.run()
