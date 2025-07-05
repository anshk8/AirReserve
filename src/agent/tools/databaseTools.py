"""
Firebase Database Tools for AirReserve
Simple store and retrieve functionality for flight search parameters (TO, FROM, maxPrice)
"""

import os
import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from langchain.tools import tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase (only once)
if not firebase_admin._apps:
    # Try to get Firebase credentials from environment or service account file
    firebase_creds_path = os.environ.get("FIREBASE_CREDENTIALS_PATH")
    
    if firebase_creds_path and os.path.exists(firebase_creds_path):
        # Use service account file
        cred = credentials.Certificate(firebase_creds_path)
    else:
        # Use default credentials (for Google Cloud environments)
        try:
            cred = credentials.ApplicationDefault()
        except Exception:
            print("Warning: Firebase credentials not configured. Database tools will not work.")
            cred = None
    
    if cred:
        firebase_admin.initialize_app(cred)

# Initialize Firestore client
try:
    db = firestore.client()
except Exception as e:
    print(f"Warning: Could not initialize Firestore client: {e}")
    db = None


@tool
def save_flight_search(to_destination: str, from_origin: str, max_price: int, user_id: str = "default") -> str:
    """
    Save flight search parameters to Firebase.
    
    Args:
        to_destination: Destination airport code or city name
        from_origin: Origin airport code or city name  
        max_price: Maximum price budget for the flight
        user_id: User identifier (optional, defaults to 'default')
    
    Returns:
        Success message with document ID or error message
    """
    if not db:
        return "Error: Firebase not configured. Please set up Firebase credentials."
    
    try:
        # Create flight search document
        flight_search_data = {
            "to": to_destination.strip().upper(),
            "from": from_origin.strip().upper(),
            "maxPrice": int(max_price),
            "userId": user_id,
            "timestamp": datetime.now()
        }
        
        # Add to Firestore collection
        doc_ref = db.collection("flight_searches").add(flight_search_data)
        doc_id = doc_ref[1].id
        
        return f"Flight search saved successfully! Document ID: {doc_id}. Searching for flights from {from_origin} to {to_destination} with max price ${max_price}"
    
    except Exception as e:
        return f"Error saving flight search: {str(e)}"


@tool
def get_flight_searches(user_id: str = "default", limit: int = 10) -> str:
    """
    Retrieve recent flight searches from Firebase.
    
    Args:
        user_id: User identifier to filter searches
        limit: Maximum number of searches to return
    
    Returns:
        JSON string of flight searches or error message
    """
    if not db:
        return "Error: Firebase not configured. Please set up Firebase credentials."
    
    try:
        # Query flight searches for user
        query = db.collection("flight_searches")\
                 .where("userId", "==", user_id)\
                 .order_by("timestamp", direction=firestore.Query.DESCENDING)\
                 .limit(limit)
        
        searches = []
        for doc in query.stream():
            search_data = doc.to_dict()
            search_data["id"] = doc.id
            # Convert timestamp to string for JSON serialization
            if "timestamp" in search_data:
                search_data["timestamp"] = search_data["timestamp"].isoformat()
            searches.append(search_data)
        
        if not searches:
            return f"No flight searches found for user {user_id}"
        
        return json.dumps(searches, indent=2)
    
    except Exception as e:
        return f"Error retrieving flight searches: {str(e)}"

