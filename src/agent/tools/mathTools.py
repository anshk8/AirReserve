#Could probablt remove this file, but maybe we might do calculations with flights

from langchain.tools import tool


# Define LangChain tools
@tool
def add_numbers(input_str: str) -> str:
    """Adds two integers. Input should be 'a,b' (e.g., '3,5') and returns the sum"""
    try:
        # Remove any extra quotes and whitespace
        input_str = input_str.replace("'", "").replace('"', '').strip()
        a, b = input_str.split(",")
        result = int(a.strip()) + int(b.strip())
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

