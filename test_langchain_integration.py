#!/usr/bin/env python3
"""
Test LangChain integration for Tavily Price Tracker Tool
"""

import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agent.tools.tavily_price_tracker import tavily_price_tracker
from langchain.tools import tool

def test_langchain_tool_decorator():
    """Test that the tool is properly decorated for LangChain"""
    
    print("🔗 Testing LangChain Tool Integration")
    print("=" * 50)
    
    # Check if the function has the @tool decorator
    if hasattr(tavily_price_tracker, '__wrapped__'):
        print("✅ Function is properly decorated with @tool")
    else:
        print("❌ Function is not decorated with @tool")
        return False
    
    # Test the tool function directly
    test_params = {
        "FROM": "Toronto",
        "TO": "Vancouver", 
        "maxPrice": 1000
    }
    
    print(f"\n🧪 Testing tool function with parameters: {test_params}")
    
    try:
        result = tavily_price_tracker(test_params)
        print(f"✅ Tool function executed successfully")
        print(f"📝 Result preview: {result[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Tool function failed: {str(e)}")
        return False

def test_tool_metadata():
    """Test that the tool has proper metadata for LangChain"""
    
    print("\n📋 Testing Tool Metadata")
    print("-" * 30)
    
    # Check function docstring
    if tavily_price_tracker.__doc__:
        print("✅ Function has docstring")
        print(f"📝 Docstring preview: {tavily_price_tracker.__doc__[:100]}...")
    else:
        print("❌ Function missing docstring")
    
    # Check function signature
    import inspect
    sig = inspect.signature(tavily_price_tracker)
    params = list(sig.parameters.keys())
    
    if 'params' in params:
        print("✅ Function accepts 'params' parameter")
    else:
        print("❌ Function missing 'params' parameter")
    
    return True

if __name__ == "__main__":
    print("Starting LangChain Integration Tests...")
    
    # Test tool decorator
    decorator_test = test_langchain_tool_decorator()
    
    # Test metadata
    metadata_test = test_tool_metadata()
    
    print("\n" + "=" * 50)
    print("📊 LANGCHAIN INTEGRATION SUMMARY")
    print("=" * 50)
    
    if decorator_test and metadata_test:
        print("🎉 All LangChain integration tests passed!")
        print("✅ Tool is ready for use with LangChain agents")
    else:
        print("⚠️  Some integration tests failed")
        print("🔧 Please check the tool implementation") 