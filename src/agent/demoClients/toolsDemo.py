#!/usr/bin/env python3
"""
Simple Demo - What Your MCP Server Actually Does
This shows the power of your MCP + LangChain setup
"""

import sys
import os
sys.path.append('.')

def demo_your_tools():
    """Demonstrate your tools working directly"""
    print("🎯 Your MCP Travel Assistant Tools Demo")
    print("=" * 50)
    
    # Import your tools directly
    from agent.MCPLangChainServer import (
        add_numbers, 
        search_destinations, 
        get_weather,
        mcp
    )
    
    print("✅ Your MCP server has loaded successfully!")
    print(f"📊 Server name: {mcp.name}")
    print(f"📊 MCP Protocol: Model Context Protocol v2024-11-05")
    
    print("\n🔧 Testing Your Tools:")
    print("-" * 30)
    
    # Test 1: Your original add tool (now MCP-compatible!)
    print("\n1️⃣ Testing add_numbers (your original tool!):")
    result = add_numbers("42,18")
    print(f"   42 + 18 = {result}")
    
    # Test 2: Search destinations
    print("\n2️⃣ Testing search_destinations:")
    result = search_destinations("japan,1200")
    print(f"   Search results:\n{result}")
    
    # Test 3: Get weather
    print("\n3️⃣ Testing get_weather:")
    result = get_weather("Tokyo")
    print(f"   {result}")
    
    # Test 4: Show MCP tools
    print("\n4️⃣ Your MCP Tools Available:")
    print("   These are what AI assistants can discover and use:")
    
    # List the MCP tools (this is what makes it special!)
    mcp_tools = [
        "add_two_numbers - Add integers (your original tool!)",
        "find_destinations - Search travel destinations by budget", 
        "check_weather - Get weather for destinations",
        "chat_with_travel_agent - Full LangChain AI conversation",
        "plan_trip - Complete trip planning with AI"
    ]
    
    for i, tool in enumerate(mcp_tools, 1):
        print(f"   {i}. {tool}")
    
    print("\n🌟 What Makes This Special:")
    print("   ✅ Your simple add tool is now part of MCP protocol")
    print("   ✅ AI assistants can automatically discover these tools")
    print("   ✅ LangChain provides intelligent tool chaining")
    print("   ✅ Industry-standard protocol for AI tool integration")
    print("   ✅ Perfect for hackathon demonstration!")
    
    print("\n🚀 How This Works in Practice:")
    print("   1. AI Assistant connects to your MCP server")
    print("   2. Discovers your 5 tools automatically")
    print("   3. Uses them intelligently based on user requests")
    print("   4. Can chain multiple tools together")
    print("   5. Provides rich, contextual responses")
    
    print("\n💡 Example AI Conversation:")
    print("   User: 'Plan a budget trip to Asia'")
    print("   AI: → Uses find_destinations(query='asia', budget=1000)")
    print("       → Uses check_weather('Thailand')")
    print("       → Uses chat_with_travel_agent('plan trip to Thailand')")
    print("       → Provides complete trip plan with costs and weather")

if __name__ == "__main__":
    demo_your_tools()
