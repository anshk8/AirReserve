#!/usr/bin/env python3
"""
MCP Connection Demo - Shows EXACTLY how client connects to server
This demonstrates the step-by-step process of MCP communication
Helps understand how MCP is linked to a client application
"""

import asyncio
import json
import subprocess
from pathlib import Path

class MCPConnectionDemo:
    def __init__(self, server_path):
        self.server_path = server_path
        self.process = None
        self.request_id = 0
        
    def get_request_id(self):
        """Get next request ID"""
        self.request_id += 1
        return self.request_id
    
    async def start_server_process(self):
        """Step 1: Start the MCP server as a subprocess"""
        print("🚀 STEP 1: Starting MCP server process...")
        print(f"   Command: /usr/local/bin/python3 {self.server_path}")
        
        # Start the server process with stdin/stdout pipes
        self.process = await asyncio.create_subprocess_exec(
            '/usr/local/bin/python3', self.server_path,
            stdin=asyncio.subprocess.PIPE,    # We write to server's stdin
            stdout=asyncio.subprocess.PIPE,   # We read from server's stdout
            stderr=asyncio.subprocess.PIPE    # Capture errors
        )
        
        print("   ✅ Server process started!")
        print(f"   📡 Communication method: stdin/stdout pipes")
        return True
    
    
    async def callTool(self, tool_name, arguments):
        """Step 5: Call a specific tool"""
        print(f"\n🔧 STEP 5: Call tool '{tool_name}'...")
        
        call_request = {
            "jsonrpc": "2.0",
            "id": self.get_request_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        response = await self.send_and_receive(call_request, f"Call Tool '{tool_name}'")
        
        if response and "result" in response:
            content = response["result"].get("content", [])
            if content and len(content) > 0:
                result = content[0].get("text", "No text result")
                print(f"   ✅ Tool result: {result}")
                return result
            else:
                print("   ⚠️ Tool returned no content")
                return "No content"
        elif response and "error" in response:
            error = response["error"]
            print(f"   ❌ Tool error: {error['message']}")
            return f"Error: {error['message']}"
        else:
            print("   ❌ Tool call failed!")
            return "Failed"
    
    async def cleanup(self):
        """Clean up the server process"""
        print("\n🧹 CLEANUP: Terminating server process...")
        if self.process:
            self.process.terminate()
            await self.process.wait()
            print("   ✅ Server terminated")

async def demo_mcp_connection():
    """Complete demonstration of MCP connection and communication"""
    print("🎯 MCP Connection & Communication Demo")
    print("=" * 60)
    print("This shows EXACTLY how your client connects to your server")
    print("=" * 60)
    
    # Path to your MCP server
    server_path = str(Path(__file__).parent / "src" / "api" / "MCPLangChainServer.py")
    
    demo = MCPConnectionDemo(server_path)
    
    try:
        # Step 1: Start server
        await demo.start_server_process()
        
        # Step 2: Initialize connection
        success = await demo.step_2_initialize()
        if not success:
            print("Server couldn't connect to Server")
            return
        
        
        # Step 4: List tools
        tools = await demo.step_4_list_tools()
        
        # Step 5: Call some tools
        if tools:
            print("\n" + "="*60)
            print("🧪 TESTING TOOL CALLS")
            print("="*60)
            
            # Test 1: Add numbers (your original tool!)
            await demo.callTool("add_two_numbers", {"numbers": "15,25"})
            
            # Test 2: Search destinations
            await demo.callTool("find_destinations", {
                "query": "thailand", 
                "budget": 1000
            })
            
            # Test 3: Get weather
            await demo.callTool("check_weather", {"destination": "Tokyo"})
        
        print("\n" + "="*60)
        print("🎉 DEMO COMPLETE!")
        print("="*60)
        print("KEY POINTS:")
        print("1. 🔌 Client starts server as subprocess")
        print("2. 📡 Communication via stdin/stdout (not HTTP!)")
        print("3. 🤝 JSON-RPC 2.0 protocol for all messages")
        print("4. 📋 Client discovers tools dynamically")
        print("5. 🔧 Client calls tools with structured parameters")
        print("6. 📤 All messages are JSON objects sent as strings")
        print("7. 📥 Server responds with JSON objects")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await demo.cleanup()

if __name__ == "__main__":
    asyncio.run(demo_mcp_connection())
