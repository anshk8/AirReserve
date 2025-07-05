"""
Firebase Realtime Database Tools for AirReserve
Simple store and retrieve functionality for flight search parameters (TO, FROM, maxPrice)
"""

import os
import json
import requests
from datetime import datetime
from langchain.tools import tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_url():
    """Get the Firebase Realtime Database URL"""
    return os.environ.get("FIREBASE_DATABASE_URL")

def _save_flight_search_impl(to_destination: str, from_origin: str, max_price: int, user_id: str = "default") -> str:
    """Internal implementation of save_flight_search without LangChain tool wrapper"""
    database_url = get_database_url()
    
    if not database_url or database_url == "https://your-project-default-rtdb.firebaseio.com/":
        return "Error: Firebase Database URL not configured. Please update FIREBASE_DATABASE_URL in your .env file."
    
    try:
        # Create flight search data
        flight_search_data = {
            "to": to_destination.strip().upper(),
            "from": from_origin.strip().upper(),
            "maxPrice": int(max_price),
            "userId": user_id,
            "timestamp": datetime.now().isoformat(),
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Send POST request to Firebase Realtime Database
        # Remove double slash in URL
        url = f"{database_url.rstrip('/')}/flight_searches.json"
        response = requests.post(url, json=flight_search_data)
        
        if response.status_code == 200:
            result = response.json()
            record_id = result.get("name", "unknown")
            return f"✅ Flight search saved successfully! Record ID: {record_id}. Searching for flights from {from_origin} to {to_destination} with max price ${max_price}"
        else:
            return f"❌ Error saving to database. Status: {response.status_code}, Response: {response.text}"
    
    except Exception as e:
        return f"❌ Error saving flight search: {str(e)}"

def _get_flight_searches_impl(user_id: str = "default", limit: int = 10) -> str:
    """Internal implementation of get_flight_searches without LangChain tool wrapper"""
    database_url = get_database_url()
    
    if not database_url or database_url == "https://your-project-default-rtdb.firebaseio.com/":
        return "Error: Firebase Database URL not configured. Please update FIREBASE_DATABASE_URL in your .env file."
    
    try:
        # Get all flight searches
        url = f"{database_url.rstrip('/')}/flight_searches.json"
        response = requests.get(url)
        
        if response.status_code == 200:
            all_data = response.json()
            
            if not all_data:
                return f"No flight searches found for user {user_id}"
            
            # Filter by user_id and convert to list
            searches = []
            for record_id, search_data in all_data.items():
                if search_data.get("userId") == user_id:
                    search_data["id"] = record_id
                    searches.append(search_data)
            
            # Sort by timestamp (newest first) and limit
            searches.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            searches = searches[:limit]
            
            if not searches:
                return f"No flight searches found for user {user_id}"
            
            return json.dumps(searches, indent=2)
        else:
            return f"❌ Error retrieving from database. Status: {response.status_code}, Response: {response.text}"
    
    except Exception as e:
        return f"❌ Error retrieving flight searches: {str(e)}"

@tool
def save_flight_search(to_destination: str, from_origin: str, max_price: int, user_id: str = "default") -> str:
    """
    Save flight search parameters to Firebase Realtime Database.
    
    Args:
        to_destination: Destination airport code or city name
        from_origin: Origin airport code or city name  
        max_price: Maximum price budget for the flight
        user_id: User identifier (optional, defaults to 'default')
    
    Returns:
        Success message with record ID or error message
    """
    return _save_flight_search_impl(to_destination, from_origin, max_price, user_id)


@tool
def get_flight_searches(user_id: str = "default", limit: int = 10) -> str:
    """
    Retrieve recent flight searches from Firebase Realtime Database.
    
    Args:
        user_id: User identifier to filter searches
        limit: Maximum number of searches to return
    
    Returns:
        JSON string of flight searches or error message
    """
    return _get_flight_searches_impl(user_id, limit)


def main():
    """Test function to insert sample data into Firebase"""
    print("🔥 Testing Firebase Database Tools")
    print("=" * 40)
    
    # Test data
    to_destination = "Canada"
    from_origin = "Toronto"  # Fixed typo
    max_price = 1000
    user_id = "test_user"
    
    print(f"📝 Inserting flight search: {from_origin} → {to_destination}, Max Price: ${max_price}")
    
    # Test save function (using internal implementation)
    result = _save_flight_search_impl(to_destination, from_origin, max_price, user_id)
    print(f"Save result: {result}")
    
    print("\n" + "="*40)
    
    # Test retrieve function
    print("📋 Retrieving flight searches...")
    result = _get_flight_searches_impl(user_id)
    print(f"Retrieve result:\n{result}")

if __name__ == "__main__":
    main()