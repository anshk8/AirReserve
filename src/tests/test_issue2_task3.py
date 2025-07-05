import sys
import os
sys.path.append('src/agent/tools')
from tavily_price_tracker import save_flight_data

# Sample data
sample_flights = [
    {
        "price": 150.00,
        "airline": "Air Canada", 
        "departure": "10:30 AM",
        "destination": "Toronto to Ottawa",
        "timestamp": "2024-01-15T10:30:00",
        "source": "Tavily Web Crawl"
    }
]

# Test the save function
result = save_flight_data(sample_flights, "Toronto", "Ottawa")
print(result)