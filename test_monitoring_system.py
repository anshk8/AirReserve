"""
Test Firebase Monitoring System
Comprehensive test to verify Firebase listener and Tavily API integration
"""

import sys
import os
import time
import json
from pathlib import Path

# Add the parent directory to sys.path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from src.agent.firebase_listener import start_firebase_listener, stop_firebase_listener, get_firebase_listener
    from src.agent.tools.databaseTools import _save_flight_search_impl
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_environment_setup():
    """Test if environment variables are properly set"""
    print("\n🔧 Testing Environment Setup")
    print("-" * 30)
    
    # Check Firebase URL
    firebase_url = os.environ.get("FIREBASE_DATABASE_URL")
    if firebase_url and firebase_url != "https://your-project-default-rtdb.firebaseio.com/":
        print("✅ Firebase URL configured")
    else:
        print("❌ Firebase URL not configured")
        return False
    
    # Check Tavily API key
    tavily_key = os.environ.get("TAVILY_API_KEY")
    if tavily_key:
        print("✅ Tavily API key configured")
    else:
        print("❌ Tavily API key not configured")
        return False
    
    return True

def test_firebase_database():
    """Test Firebase database connectivity"""
    print("\n🔥 Testing Firebase Database")
    print("-" * 30)
    
    try:
        # Try to save a test flight search
        result = _save_flight_search_impl(
            to_destination="TEST_DEST",
            from_origin="TEST_ORIGIN", 
            max_price=999,
            user_id="test_monitoring"
        )
        
        if "saved successfully" in result:
            print("✅ Firebase database write test passed")
            return True
        else:
            print(f"❌ Firebase database write test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Firebase database test error: {str(e)}")
        return False

def test_tavily_api():
    """Test LangChain agent with Tavily API"""
    print("\n🌐 Testing LangChain Agent with Tavily API")
    print("-" * 40)
    
    try:
        # Import the agent from MCP server
        from src.agent.MCPLangChainServer import agent
        
        if not agent:
            print("❌ LangChain agent not initialized (missing OpenAI API key)")
            return False
        
        # Test with a simple flight search using agent
        prompt = "Get me flights from Toronto to Vancouver under $500"
        response = agent.invoke({"input": prompt})
        result = response.get("output", "No response from agent")
        
        if "Error" not in result:
            print("✅ LangChain agent test passed")
            print(f"   Sample result: {result[:100]}...")
            return True
        else:
            print(f"❌ LangChain agent test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ LangChain agent test error: {str(e)}")
        return False

def test_firebase_monitoring():
    """Test Firebase monitoring system with LangChain agent"""
    print("\n📡 Testing Firebase Monitoring System with LangChain Agent")
    print("-" * 55)
    
    try:
        # Import agent from MCP server
        from src.agent.MCPLangChainServer import agent
        
        if not agent:
            print("❌ LangChain agent not available - skipping monitoring test")
            return False
        
        # Start the listener with agent
        print("Starting Firebase listener with LangChain agent...")
        listener = start_firebase_listener(agent=agent, poll_interval=2)
        
        # Wait a moment for listener to initialize
        time.sleep(3)
        
        # Check status
        status = listener.get_status()
        if status["is_running"]:
            print("✅ Firebase listener started successfully")
            print(f"   Status: {json.dumps(status, indent=2)}")
        else:
            print("❌ Firebase listener failed to start")
            return False
        
        # Add a test flight search that should trigger the listener
        print("\n📝 Adding test flight search to trigger agent...")
        result = _save_flight_search_impl(
            to_destination="Paris",
            from_origin="Toronto", 
            max_price=800,
            user_id="monitoring_test"
        )
        print(f"   Database result: {result}")
        
        # Wait for the listener to process
        print("\n⏳ Waiting 10 seconds for agent to detect and process...")
        time.sleep(10)
        
        # Check updated status
        updated_status = listener.get_status()
        print(f"\n📊 Updated status: {json.dumps(updated_status, indent=2)}")
        
        # Stop the listener
        print("\n🛑 Stopping Firebase listener...")
        stop_firebase_listener()
        print("✅ Firebase monitoring test with agent completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Firebase monitoring test error: {str(e)}")
        try:
            stop_firebase_listener()
        except:
            pass
        return False

def run_full_test():
    """Run the complete test suite"""
    print("🧪 AirReserve Monitoring System Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Firebase Database", test_firebase_database),
        ("LangChain Agent", test_tavily_api),
        ("Firebase Monitoring", test_firebase_monitoring)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your monitoring system is ready to use.")
        print("\n💡 To start monitoring:")
        print("   python start_monitoring.py")
        print("\n💡 Or use the MCP server tools:")
        print("   start_monitoring_firebase()")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues before using the system.")

if __name__ == "__main__":
    run_full_test()
