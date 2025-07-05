#!/usr/bin/env python3
"""
Simple MCP Python Client - Chatbot Style
Uses your MCP tools directly in a conversational interface
Run this and see how this as a client can use MCP Server tools
"""

import sys
import os
sys.path.append('.')

def create_chatbot():
    """Create a simple chatbot using your MCP tools"""
    
    # Import your tools directly
    from agent.MCPLangChainServer import (
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
            
            # Handle add command
            elif user_input.lower().startswith('add '):
                numbers = user_input[4:].strip()
                try:
                    result = add_numbers(numbers)
                    print(f"🔢 Result: {result}")
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            # Handle search command
            elif user_input.lower().startswith('search '):
                search_params = user_input[7:].strip()
                try:
                    result = search_destinations(search_params)
                    print(f"🌍 Search Results:\n{result}")
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            # Handle weather command
            elif user_input.lower().startswith('weather '):
                destination = user_input[8:].strip()
                try:
                    result = get_weather(destination)
                    print(f"🌤️ {result}")
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            # Handle chat command (AI agent)
            elif user_input.lower().startswith('chat '):
                message = user_input[5:].strip()
                try:
                    if agent:
                        print("🤖 AI Agent is thinking...")
                        response = agent.invoke({"input": message})
                        ai_response = response.get("output", "No response from agent")
                        print(f"🤖 AI Agent: {ai_response}")
                    else:
                        print("❌ AI Agent not available (OpenAI API key not set)")
                except Exception as e:
                    print(f"❌ AI Agent Error: {e}")
            
            # Handle natural language (try to parse intent)
            else:
                print("🤔 I'm not sure what you want. Try:")
                print("  - 'add 5,10' for math")
                print("  - 'search paris,1500' for destinations")
                print("  - 'weather tokyo' for weather")
                print("  - 'chat plan a trip to Japan' for AI help")
                print("  - 'help' for more commands")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    create_chatbot()
