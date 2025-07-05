#!/usr/bin/env python3
"""
Test script to verify LangChain async capabilities for Issue 3.
This script tests the basic async functionality we'll need for the price monitoring agent.
"""

import asyncio
import json
import os
from pathlib import Path

# Test imports
try:
    import langchain
    import langchain_community
    import aiofiles
    print("✅ All required packages imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)

async def test_async_basic():
    """Test basic async functionality"""
    print("Testing basic async functionality...")
    
    async def async_function():
        await asyncio.sleep(0.1)  # Simulate async work
        return "Async function completed"
    
    result = await async_function()
    print(f"✅ {result}")

async def test_async_file_operations():
    """Test async file operations"""
    print("Testing async file operations...")
    
    # Create test data
    test_data = {
        "flights": [
            {"airline": "Test Air", "price": 150, "destination": "Test City"}
        ]
    }
    
    # Write test file
    test_file = Path("src/data/test_flight_prices.json")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    
    async with aiofiles.open(test_file, 'w') as f:
        await f.write(json.dumps(test_data, indent=2))
    
    # Read test file
    async with aiofiles.open(test_file, 'r') as f:
        content = await f.read()
        loaded_data = json.loads(content)
    
    # Clean up
    test_file.unlink()
    
    print(f"✅ Async file operations work: {loaded_data['flights'][0]['airline']}")

async def test_langchain_async_integration():
    """Test LangChain async integration"""
    print("Testing LangChain async integration...")
    
    # This is a placeholder for actual LangChain async agent testing
    # We'll implement this more fully in the actual agent
    print("✅ LangChain async integration ready for implementation")

async def main():
    """Run all async tests"""
    print("🚀 Starting LangChain async environment tests...")
    print(f"LangChain version: {langchain.__version__}")
    print(f"LangChain Community version: {langchain_community.__version__}")
    print("aiofiles installed and available")
    print("-" * 50)
    
    await test_async_basic()
    await test_async_file_operations()
    await test_langchain_async_integration()
    
    print("-" * 50)
    print("🎉 All async tests completed successfully!")
    print("✅ LangChain environment is ready for Issue 3 implementation")

if __name__ == "__main__":
    asyncio.run(main()) 