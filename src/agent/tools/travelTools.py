
#TOOLS RELATED TO TRAVEL, TAVILY ETC CAN GO HERE


from langchain.tools import tool

@tool  
def search_destinations(input_str: str) -> str:
    """Search for travel destinations based on query and budget. Input format: 'query,budget' (e.g., 'paris,1500')"""
    try:
        # Parse input string
        if ',' in input_str:
            query, budget_str = input_str.split(',', 1)
            query = query.strip()
            budget = float(budget_str.strip())
        else:
            query = input_str.strip()
            budget = 2000.0  # default budget
        
        # Mock travel search (replace with real API)
        destinations = [
            {"name": "Paris", "price": 1200, "rating": 4.5},
            {"name": "Tokyo", "price": 1500, "rating": 4.7},
            {"name": "Bali", "price": 800, "rating": 4.3},
            {"name": "New York", "price": 1000, "rating": 4.4},
            {"name": "Barcelona", "price": 900, "rating": 4.2},
            {"name": "Thailand", "price": 700, "rating": 4.4}
        ]
        
        # Filter by budget and query
        filtered = []
        for dest in destinations:
            if dest["price"] <= budget:
                if not query or query.lower() in dest["name"].lower():
                    filtered.append(dest)
        
        if not filtered:
            return f"No destinations found for '{query}' within budget of ${budget}"
        
        result = f"Found {len(filtered)} destinations for '{query}' within ${budget}:\n"
        for dest in filtered:
            result += f"- {dest['name']}: ${dest['price']} (Rating: {dest['rating']}⭐)\n"
        
        return result
    except Exception as e:
        return f"Error searching destinations: {str(e)}"
