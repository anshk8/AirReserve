"""
Single-input wrapper tools for LangChain agent compatibility
These tools accept a single string input and parse the parameters
"""

from langchain.tools import tool
from .databaseTools import _save_flight_search_impl, _get_flight_searches_impl
from .tavily_price_tracker import tavily_price_tracker

@tool
def save_flight_search_simple(input_string: str) -> str:
    """
    Save flight search parameters to Firebase database.
    
    Args:
        input_string: Comma-separated values: "destination,origin,max_price,user_id"
                     Example: "Paris,New York,800,user123"
    
    Returns:
        Success message with document ID or error message
    """
    try:
        parts = input_string.split(',')
        if len(parts) < 3:
            return "❌ Error: Please provide at least destination,origin,max_price (comma-separated)"
        
        to_destination = parts[0].strip()
        from_origin = parts[1].strip()
        max_price = int(parts[2].strip())
        user_id = parts[3].strip() if len(parts) > 3 else "default"
        
        return _save_flight_search_impl(to_destination, from_origin, max_price, user_id)
    except ValueError:
        return "❌ Error: max_price must be a valid number"
    except Exception as e:
        return f"❌ Error parsing input: {str(e)}"

@tool
def get_flight_searches_simple(input_string: str) -> str:
    """
    Retrieve recent flight searches from Firebase database.
    
    Args:
        input_string: Format "user_id,limit" or just "user_id"
                     Example: "user123,5" or "user123"
    
    Returns:
        JSON string of flight searches or error message
    """
    try:
        parts = input_string.split(',')
        user_id = parts[0].strip() if parts[0].strip() else "default"
        limit = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip() else 10
        
        return _get_flight_searches_impl(user_id, limit)
    except ValueError:
        return "❌ Error: limit must be a valid number"
    except Exception as e:
        return f"❌ Error parsing input: {str(e)}"

@tool  
def search_flight_prices_simple(input_string: str) -> str:
    """
    Search for flight prices using Tavily API.
    
    Args:
        input_string: Comma-separated values: "from_city,to_city,max_price"
                     Example: "New York,London,600"
    
    Returns:
        Flight price information from Tavily API
    """
    try:
        parts = input_string.split(',')
        if len(parts) < 3:
            return "❌ Error: Please provide from_city,to_city,max_price (comma-separated)"
        
        from_city = parts[0].strip()
        to_city = parts[1].strip()
        max_price = parts[2].strip()
        
        return tavily_price_tracker.invoke({
            "from_city": from_city,
            "to_city": to_city,
            "max_price": max_price
        })

        return 
    except Exception as e:
        return f"❌ Error searching flights: {str(e)}"
