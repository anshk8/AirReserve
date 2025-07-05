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
from .tools.mathTools import add_numbers
from .tools.travelTools import search_destinations
from SYSTEMPROMPT import system_prompt

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


#Can remove thus after just for testing
@tool
def get_weather(destination: str) -> str:
    """Get weather information for a destination. If no destination is provided or destination is unclear, ask the user to specify."""
    # Check if destination is provided and valid
    if not destination or destination.strip().lower() in ['', 'unknown', 'none', 'null']:
        return "I need to know which destination you'd like weather information for. Please specify a city or location."
    
    # Mock weather data (replace with real weather API)
    weather_data = {
        "paris": "Sunny, 22°C (72°F). Perfect weather for sightseeing!",
        "tokyo": "Cloudy, 18°C (64°F). Light jacket recommended.", 
        "bali": "Tropical, 28°C (82°F). Warm and humid with occasional showers.",
        "new york": "Rainy, 15°C (59°F). Bring an umbrella!",
        "barcelona": "Mild, 25°C (77°F). Beautiful Mediterranean weather.",
        "thailand": "Hot and humid, 32°C (90°F). Stay hydrated!"
    }
    
    result = weather_data.get(destination.lower(), f"Weather data not available for {destination}")
    return f"Weather in {destination}: {result}"

# Initialize LangChain agent with tools
if llm:

    # Memory important so we can ask follow ups
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    #tools are imports from tools/ folder
    langchain_tools = [add_numbers, search_destinations, get_weather]

    

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

# MCP Tool Definitions
@mcp.tool()
def add_two_numbers(numbers: str) -> str:
    """Add two integers together.
    
    Args:
        numbers: Two numbers separated by comma (e.g., '3,5')
    
    Returns:
        The sum as a string
    """
    return add_numbers(numbers)

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
def check_weather(destination: str) -> str:
    """Get current weather information for a destination.
    
    Args:
        destination: Name of the destination
    
    Returns:
        Weather information for the destination
    """
    return get_weather(destination)

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


# RESOURCES we will likely need TODO LATER
@mcp.resource("travel://destinations")
def get_destinations_data():
    """Get the travel destinations database"""
    return json.dumps({
        "destinations": [
            {"name": "Paris", "country": "France", "price": 1200, "rating": 4.5},
            {"name": "Tokyo", "country": "Japan", "price": 1500, "rating": 4.7},
            {"name": "Bali", "country": "Indonesia", "price": 800, "rating": 4.3},
            {"name": "New York", "country": "USA", "price": 1000, "rating": 4.4},
            {"name": "Barcelona", "country": "Spain", "price": 900, "rating": 4.2},
            {"name": "Thailand", "country": "Thailand", "price": 700, "rating": 4.4}
        ]
    })

if __name__ == "__main__":
    # Run the server
    mcp.run()
