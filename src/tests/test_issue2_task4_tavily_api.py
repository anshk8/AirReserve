#!/usr/bin/env python3
"""
Test script for Issue 2 Task 4: Testing & Validation
Tests Tavily API integration with real flight routes
"""

import sys
import os
import json
from datetime import datetime

# Add the tools directory to path
sys.path.append('src/agent/tools')

# Import the main tool function
from tavily_price_tracker import tavily_price_tracker

def test_tavily_api_integration():
    """Test the Tavily API integration with real flight routes"""
    
    print("🧪 Task 4: Testing Tavily API Integration")
    print("=" * 60)
    
    # Test routes from the task list
    test_routes = [
        {"FROM": "Toronto", "TO": "Ottawa", "maxPrice": 700},
        {"FROM": "Ottawa", "TO": "Montreal", "maxPrice": 850},
        {"FROM": "Vancouver", "TO": "Calgary", "maxPrice": 900},
    ]
    
    print(f"📋 Testing {len(test_routes)} flight routes:")
    for i, route in enumerate(test_routes, 1):
        print(f"   {i}. {route['FROM']} → {route['TO']} (max: ${route['maxPrice']})")
    
    print("\n�� Starting API tests...")
    print("-" * 40)
    
    results = []
    
    for i, route in enumerate(test_routes, 1):
        print(f"\n�� Test {i}: {route['FROM']} → {route['TO']}")
        print(f"   Max price: ${route['maxPrice']}")
        
        try:
            # Call the Tavily API tool
            result = tavily_price_tracker(route)
            
            # Check if it was successful
            if "✅ Found" in result or "❌ No flights found" in result:
                print(f"   ✅ API call successful")
                print(f"   📊 Result: {result[:100]}...")
                
                # Check if data was saved
                if "Flight data saved to" in result or "Flight data appended to" in result:
                    print(f"   💾 Data storage: SUCCESS")
                else:
                    print(f"   ❌ Data storage: FAILED")
                    
            elif "Error:" in result:
                print(f"   ❌ API call failed: {result}")
            else:
                print(f"   ⚠️  Unexpected response: {result[:100]}...")
                
            results.append({
                "route": f"{route['FROM']} → {route['TO']}",
                "success": "✅ Found" in result or "❌ No flights found" in result,
                "result": result
            })
            
        except Exception as e:
            print(f"   ❌ Exception occurred: {e}")
            results.append({
                "route": f"{route['FROM']} → {route['TO']}",
                "success": False,
                "result": f"Exception: {e}"
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("�� TEST SUMMARY")
    print("=" * 60)
    
    successful_tests = sum(1 for r in results if r["success"])
    total_tests = len(results)
    
    print(f"✅ Successful tests: {successful_tests}/{total_tests}")
    print(f"❌ Failed tests: {total_tests - successful_tests}/{total_tests}")
    
    # Check data files
    print(f"\n📁 Checking data files...")
    data_dir = "data"
    if os.path.exists(data_dir):
        files = os.listdir(data_dir)
        json_files = [f for f in files if f.endswith('.json')]
        flight_files = [f for f in json_files if f.startswith('flight_prices_')]
        
        print(f"   📄 Total JSON files: {len(json_files)}")
        print(f"   ✈️  Flight price files: {len(flight_files)}")
        
        if flight_files:
            print(f"   📋 Latest files:")
            for file in sorted(flight_files)[-3:]:  # Show last 3 files
                file_path = os.path.join(data_dir, file)
                file_size = os.path.getsize(file_path)
                print(f"      - {file} ({file_size} bytes)")
    
    # Final assessment
    print(f"\n🎯 TASK 4 ASSESSMENT:")
    if successful_tests >= 2:  # At least 2 out of 3 tests should work
        print(f"   ✅ Task 4: PASSED - API integration working")
        print(f"   ✅ Ready for Task 5: Documentation")
    else:
        print(f"   ❌ Task 4: NEEDS WORK - API integration issues")
        print(f"   🔧 Check API key and network connectivity")
    
    return successful_tests >= 2

def test_error_handling():
    """Test error handling scenarios"""
    
    print(f"\n🔧 Testing Error Handling")
    print("-" * 40)
    
    # Test 1: Missing parameters
    print(f"Test 1: Missing parameters")
    try:
        result = tavily_price_tracker({"FROM": "Toronto"})  # Missing TO and maxPrice
        print(f"   Result: {result}")
        if "Error: Missing required parameters" in result:
            print(f"   ✅ Error handling: PASSED")
        else:
            print(f"   ❌ Error handling: FAILED")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 2: Invalid maxPrice
    print(f"Test 2: Invalid maxPrice")
    try:
        result = tavily_price_tracker({"FROM": "Toronto", "TO": "Ottawa", "maxPrice": "invalid"})
        print(f"   Result: {result}")
        if "Error: maxPrice must be a valid integer" in result:
            print(f"   ✅ Error handling: PASSED")
        else:
            print(f"   ❌ Error handling: FAILED")
    except Exception as e:
        print(f"   ❌ Exception: {e}")

if __name__ == "__main__":
    print("Starting Task 4: Testing & Validation")
    print("Make sure you have TAVILY_API_KEY set in your environment!")
    print()
    
    # Test main functionality
    main_success = test_tavily_api_integration()
    
    # Test error handling
    test_error_handling()
    
    if main_success:
        print(f"\n🎉 Task 4: Testing & Validation - COMPLETED!")
    else:
        print(f"\n⚠️  Task 4: Testing & Validation - NEEDS ATTENTION!")