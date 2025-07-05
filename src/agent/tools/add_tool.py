from langchain.tools import tool
import requests

@tool
def add_tool(input_str: str) -> str:
    "Adds two integers. Input should be 'a,b' (e.g., '3,5') and would return 8"
    # Remove any extra quotes and whitespace
    input_str = input_str.replace("'", "").replace('"', '').strip()
    a, b = input_str.split(",")
    res = int(a.strip()) + int(b.strip())
    print(res)
    return str(res)


