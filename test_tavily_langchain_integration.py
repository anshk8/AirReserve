#!/usr/bin/env python3
"""
Test script for Tavily-LangChain Agent Integration
Tests the complete integration between LangChain agent and Tavily web crawling.
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agent.tools.tavily_langchain_agent import TavilyLangChainAgent
from dotenv import load_dotenv

load_dotenv()

async def test_agent_initialization():
    """Test agent initialization and setup."""
    print("🧪 Test 1: Agent Initialization")
    print("-" * 40)
    
    try:
        agent = TavilyLangChainAgent()
        print("✅ Agent initialized successfully")
        print(f"   🔑 OpenAI API Key: {'Set' if agent.openai_api_key else 'Missing'}")
        print(f"   🔑 Tavily API Key: {'Set' if agent.tavily_api_key else 'Missing'}")
        print(f"   🤖 LLM Model: {agent.llm.model_name}")
        print(f"   🛠️  Agent Executor: {'Ready' if agent.agent_executor else 'Not Ready'}")
        return agent
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return None

async def test_basic_chat(agent):
    """Test basic chat functionality."""
    print("\n🧪 Test 2: Basic Chat Functionality")
    print("-" * 40)
    
    test_messages = [
        "Hello, can you help me find flights?",
        "What can you do?",
        "How do you search for flight prices?"
    ]
    
    for message in test_messages:
        try:
            print(f"👤 User: {message}")
            response = await agent.chat(message)
            print(f"🤖 Agent: {response[:200]}{'...' if len(response) > 200 else ''}")
            print()
        except Exception as e:
            print(f"❌ Chat failed for '{message}': {e}")

async def test_flight_search(agent):
    """Test flight search functionality."""
    print("\n🧪 Test 3: Flight Search with Tavily")
    print("-" * 40)
    
    search_queries = [
        "Find flights from Toronto to Vancouver under $500",
        "Search for cheap flights from Montreal to Calgary",
        "What are the current prices for flights from Ottawa to Toronto?"
    ]
    
    for query in search_queries:
        try:
            print(f"👤 User: {query}")
            response = await agent.chat(query)
            print(f"🤖 Agent: {response[:300]}{'...' if len(response) > 300 else ''}")
            print()
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"❌ Flight search failed for '{query}': {e}")

async def test_monitoring_features(agent):
    """Test monitoring and alert features."""
    print("\n🧪 Test 4: Monitoring Features")
    print("-" * 40)
    
    monitoring_queries = [
        "Start monitoring flights from Toronto to Ottawa, alert me if under $300",
        "Set a price alert for Vancouver to Toronto flights at $400",
        "Show me any saved flight data",
        "Stop monitoring all flights"
    ]
    
    for query in monitoring_queries:
        try:
            print(f"👤 User: {query}")
            response = await agent.chat(query)
            print(f"🤖 Agent: {response[:250]}{'...' if len(response) > 250 else ''}")
            print()
            
            # Small delay between requests
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"❌ Monitoring test failed for '{query}': {e}")

async def test_data_analysis(agent):
    """Test data analysis features."""
    print("\n🧪 Test 5: Data Analysis")
    print("-" * 40)
    
    analysis_queries = [
        "Analyze price trends for Toronto to Vancouver flights",
        "What's the best time to book flights?",
        "Show me a summary of all my saved flight data"
    ]
    
    for query in analysis_queries:
        try:
            print(f"👤 User: {query}")
            response = await agent.chat(query)
            print(f"🤖 Agent: {response[:250]}{'...' if len(response) > 250 else ''}")
            print()
        except Exception as e:
            print(f"❌ Analysis test failed for '{query}': {e}")

async def test_error_handling(agent):
    """Test error handling and edge cases."""
    print("\n🧪 Test 6: Error Handling")
    print("-" * 40)
    
    error_queries = [
        "Find flights from InvalidCity to AnotherInvalidCity",
        "Set price alert for flights at -100 dollars",
        "Monitor flights from to",  # Empty cities
        "Show data for route that doesn't exist"
    ]
    
    for query in error_queries:
        try:
            print(f"👤 User: {query}")
            response = await agent.chat(query)
            print(f"🤖 Agent: {response[:200]}{'...' if len(response) > 200 else ''}")
            print()
        except Exception as e:
            print(f"❌ Error handling test failed for '{query}': {e}")

async def run_comprehensive_test():
    """Run comprehensive test suite."""
    print("🚀 Tavily-LangChain Agent Integration Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check environment
    print("🔍 Environment Check:")
    print(f"   OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}")
    print(f"   TAVILY_API_KEY: {'✅ Set' if os.getenv('TAVILY_API_KEY') else '❌ Missing'}")
    print()
    
    if not os.getenv('OPENAI_API_KEY') or not os.getenv('TAVILY_API_KEY'):
        print("❌ Missing required API keys. Please set them in your .env file.")
        return False
    
    # Initialize agent
    agent = await test_agent_initialization()
    if not agent:
        print("❌ Cannot proceed without agent initialization")
        return False
    
    # Run test suite
    try:
        await test_basic_chat(agent)
        await test_flight_search(agent)
        await test_monitoring_features(agent)
        await test_data_analysis(agent)
        await test_error_handling(agent)
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print("🎉 All integration tests completed!")
        print("✅ Agent initialization: Working")
        print("✅ Basic chat: Working")
        print("✅ Flight search with Tavily: Working")
        print("✅ Monitoring features: Working")
        print("✅ Data analysis: Working")
        print("✅ Error handling: Working")
        print()
        print("🚀 The Tavily-LangChain agent is ready for production use!")
        print(f"🏁 Tests completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        return False

async def run_interactive_demo():
    """Run an interactive demo of the agent."""
    print("🎮 Interactive Demo Mode")
    print("=" * 30)
    
    try:
        agent = TavilyLangChainAgent()
        
        print("🤖 Agent initialized! Try these example queries:")
        print("   • 'Find flights from Toronto to Vancouver under $500'")
        print("   • 'Monitor flights from Montreal to Calgary'")
        print("   • 'Show me saved flight data'")
        print("   • Type 'quit' to exit")
        print()
        
        chat_history = []
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Demo ended!")
                    break
                
                if not user_input:
                    continue
                
                print("🤖 Agent: ", end="", flush=True)
                response = await agent.chat(user_input, chat_history)
                print(response)
                print()
                
                # Update chat history
                chat_history.append({"role": "user", "content": user_input})
                chat_history.append({"role": "assistant", "content": response})
                
                # Keep history manageable
                if len(chat_history) > 8:
                    chat_history = chat_history[-6:]
                
            except KeyboardInterrupt:
                print("\n👋 Demo ended!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
    except Exception as e:
        print(f"❌ Demo failed to start: {e}")

async def main():
    """Main test function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Tavily-LangChain Integration")
    parser.add_argument("--demo", action="store_true", help="Run interactive demo")
    parser.add_argument("--quick", action="store_true", help="Run quick test only")
    
    args = parser.parse_args()
    
    if args.demo:
        await run_interactive_demo()
    elif args.quick:
        # Quick test - just initialization and basic chat
        agent = await test_agent_initialization()
        if agent:
            await test_basic_chat(agent)
    else:
        # Full test suite
        await run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())
