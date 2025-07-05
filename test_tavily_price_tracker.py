#!/usr/bin/env python3
"""
Test script for Tavily Price Tracker Tool
Tests the functionality with sample routes as specified in Issue 2 task list
"""

import sys
import os
from datetime import datetime

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agent.tools.tavily_price_tracker import tavily_price_tracker

def test_flight_price_tracker():
    """Test the Tavily price tracker with sample routes"""
    
    print("🚀 Testing Tavily Price Tracker Tool")
    print("=" * 50)
    
    # Test cases as specified in the task list
    test_cases = [
        {
            "name": "Toronto → Ottawa",
            "params": {"FROM": "Toronto", "TO": "Ottawa", "maxPrice": 300}
        },
        {
            "name": "Ottawa → Montreal", 
            "params": {"FROM": "Ottawa", "TO": "Montreal", "maxPrice": 250}
        },
        {
            "name": "Vancouver → Toronto",
            "params": {"FROM": "Vancouver", "TO": "Toronto", "maxPrice": 800}
        },
        {
            "name": "Calgary → Edmonton",
            "params": {"FROM": "Calgary", "TO": "Edmonton", "maxPrice": 200}
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print(f"   Parameters: {test_case['params']}")
        print("-" * 40)
        
        try:
            # Call the tool function with individual parameters using invoke
            params = test_case['params']
            result = tavily_price_tracker.invoke({
                "from_city": params["FROM"],
                "to_city": params["TO"], 
                "max_price": str(params["maxPrice"])
            })
            
            # Store result
            test_result = {
                "test_name": test_case['name'],
                "params": test_case['params'],
                "result": result,
                "success": "Error:" not in result[:10],  # Simple success check
                "timestamp": datetime.now().isoformat()
            }
            results.append(test_result)
            
            # Display result
            print(f"✅ Result: {result}")
            
        except Exception as e:
            error_msg = f"❌ Test failed with exception: {str(e)}"
            print(error_msg)
            
            test_result = {
                "test_name": test_case['name'],
                "params": test_case['params'],
                "result": error_msg,
                "success": False,
                "timestamp": datetime.now().isoformat()
            }
            results.append(test_result)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    successful_tests = sum(1 for r in results if r['success'])
    total_tests = len(results)
    
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    
    # Detailed results
    print("\n📋 DETAILED RESULTS:")
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{status} {result['test_name']}")
        if not result['success']:
            print(f"   Error: {result['result'][:100]}...")
    
    # Check for data files
    print("\n📁 CHECKING DATA FILES:")
    data_dir = "data"
    if os.path.exists(data_dir):
        files = [f for f in os.listdir(data_dir) if f.startswith("flight_prices_")]
        if files:
            print(f"✅ Found {len(files)} flight price data files:")
            for file in files:
                file_path = os.path.join(data_dir, file)
                file_size = os.path.getsize(file_path)
                print(f"   📄 {file} ({file_size} bytes)")
        else:
            print("⚠️  No flight price data files found")
    else:
        print("❌ Data directory not found")
    
    return results

def test_error_handling():
    """Test error handling scenarios"""
    
    print("\n🔧 TESTING ERROR HANDLING")
    print("=" * 50)
    
    error_test_cases = [
        {
            "name": "Missing Parameters",
            "params": {"FROM": "Toronto"},  # Missing TO and maxPrice
            "expected_error": "Missing required parameters"
        },
        {
            "name": "Invalid maxPrice",
            "params": {"FROM": "Toronto", "TO": "Ottawa", "maxPrice": "invalid"},
            "expected_error": "max_price must be a valid integer"
        },
        {
            "name": "Empty Parameters",
            "params": {"FROM": "", "TO": "", "maxPrice": 100},
            "expected_error": "Missing required parameters"
        }
    ]
    
    for test_case in error_test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        print(f"   Parameters: {test_case['params']}")
        
        try:
            params = test_case['params']
            result = tavily_price_tracker.invoke({
                "from_city": params.get("FROM", ""),
                "to_city": params.get("TO", ""),
                "max_price": str(params.get("maxPrice", ""))
            })
            expected_error = test_case['expected_error']
            
            if expected_error in result:
                print(f"✅ PASS: Correctly handled error - {expected_error}")
            else:
                print(f"❌ FAIL: Expected '{expected_error}' but got: {result[:100]}...")
                
        except Exception as e:
            print(f"❌ FAIL: Unexpected exception: {str(e)}")

if __name__ == "__main__":
    print("Starting Tavily Price Tracker Tests...")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run main tests
    test_results = test_flight_price_tracker()
    
    # Run error handling tests
    test_error_handling()
    
    print(f"\n🏁 All tests completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") 