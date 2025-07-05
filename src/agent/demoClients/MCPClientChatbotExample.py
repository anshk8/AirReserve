#!/usr/bin/env python3
"""
Simple MCP Python Client - Chatbot Style
Uses your MCP tools directly in a conversational interface
Run this and see how this as a client can use MCP Server tools
"""

import sys
import os
sys.path.append('.')
sys.path.append('../..')  # Add path to reach src directory

def create_chatbot():
    """Create a simple chatbot using your MCP tools"""
    
    # Import your tools directly
    from src.agent.MCPLangChainServer import (
        add_numbers, 
        search_destinations, 
        get_weather,
        agent
    )
    
    print("🤖 MCP Travel Assistant Chatbot")
    print("=" * 40)
    print("Available commands:")
    print("  - 'add 5,10' - Add two numbers")
    print("  - 'search paris,1500' - Search destinations")
    print("  - 'weather tokyo' - Get weather")
    print("  - 'chat <message>' - Talk with AI agent")
    print("  - 'help' - Show this help")
    print("  - 'exit' - Quit")
    print("=" * 40)
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if not user_input:
                continue
                
            # Handle exit
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("👋 Goodbye!")
                break
            
            # Handle help
            elif user_input.lower() == 'help':
                print("📋 Available commands:")
                print("  - add <num1>,<num2> - Add two numbers")
                print("  - search <destination>,<budget> - Search destinations")
                print("  - weather <destination> - Get weather")
                print("  - chat <message> - Talk with AI agent")
                continue
            
            agent.invoke(user_input)
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    create_chatbot()
