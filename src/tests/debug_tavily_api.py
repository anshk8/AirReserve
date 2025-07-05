#!/usr/bin/env python3
"""
Debug script for Tavily API key issues
"""

import os
import requests
import json
from dotenv import load_dotenv

def debug_tavily_api():
    """Debug Tavily API key and connection issues"""
    
    print("🔍 Tavily API Debug Diagnostic")
    print("=" * 50)
    
    # Step 1: Check environment loading
    print("1. Checking environment variables...")
    load_dotenv()
    
    api_key = os.getenv("TAVILY_API_KEY")
    if api_key:
        print(f"   ✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
        print(f"   📏 Key length: {len(api_key)} characters")
        
        # Check for common issues
        if api_key.startswith("tvly-"):
            print(f"   ✅ Key format looks correct (starts with 'tvly-')")
        else:
            print(f"   ⚠️  Key format might be wrong (should start with 'tvly-')")
            
        if " " in api_key:
            print(f"   ❌ Key contains spaces - this will cause issues!")
        else:
            print(f"   ✅ Key has no spaces")
            
    else:
        print(f"   ❌ No API key found in environment")
        return False
    
    # Step 2: Test basic API call
    print(f"\n2. Testing basic API call...")
    
    url = "https://api.tavily.com/search"
    data = {
        "query": "test query",
        "search_depth": "basic"
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"   🌐 Making request to: {url}")
        print(f"   📝 Query: 'test query'")
        print(f"   🔑 Using Authorization header with Bearer token")
        
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        print(f"   📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ API call successful!")
            data = response.json()
            print(f"   📄 Response keys: {list(data.keys())}")
            return True
            
        elif response.status_code == 401:
            print(f"   ❌ Unauthorized (401) - API key issue")
            print(f"   📄 Response: {response.text[:200]}...")
            
            # Try to parse error details
            try:
                error_data = response.json()
                if "detail" in error_data:
                    print(f"   🔍 Error detail: {error_data['detail']}")
            except:
                pass
                
        elif response.status_code == 403:
            print(f"   ❌ Forbidden (403) - Permission issue")
            print(f"   📄 Response: {response.text[:200]}...")
            
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
            print(f"   📄 Response: {response.text[:200]}...")
            
    except requests.exceptions.Timeout:
        print(f"   ❌ Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
    
    # Step 3: Test alternative endpoint
    print(f"\n3. Testing alternative endpoint...")
    
    try:
        # Try the search endpoint with different parameters
        search_url = "https://api.tavily.com/search"
        search_data = {
            "query": "test",
            "search_depth": "basic",
            "include_answer": True
        }
        
        search_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        print(f"   🌐 Trying search endpoint with different params: {search_url}")
        search_response = requests.post(search_url, json=search_data, headers=search_headers, timeout=10)
        
        print(f"   📊 Search Status: {search_response.status_code}")
        if search_response.status_code == 200:
            print(f"   ✅ Search endpoint works with POST method!")
        else:
            print(f"   ❌ Search endpoint failed: {search_response.text[:100]}...")
            
    except Exception as e:
        print(f"   ❌ Search endpoint test failed: {e}")
    
    # Step 4: Recommendations
    print(f"\n4. Recommendations:")
    
    if response.status_code == 401:
        print(f"   🔑 Get a new API key from: https://tavily.com/")
        print(f"   🔑 Make sure the key starts with 'tvly-'")
        print(f"   🔑 Check if the key has web-crawl permissions")
        
    elif response.status_code == 403:
        print(f"   🔑 Check API key permissions in Tavily dashboard")
        print(f"   🔑 Verify the key has access to web-crawl feature")
        
    else:
        print(f"   🔑 Check network connectivity")
        print(f"   🔑 Verify Tavily service status")
    
    return False

if __name__ == "__main__":
    success = debug_tavily_api()
    
    if success:
        print(f"\n🎉 API key is working! The issue might be in our flight search code.")
    else:
        print(f"\n⚠️  API key needs attention. Check the recommendations above.") 