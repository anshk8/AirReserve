#!/usr/bin/env python3
"""
CLI Runner for Tavily-LangChain Flight Price Agent
Simple script to run the integrated agent with proper environment setup.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agent.tools.tavily_langchain_agent import main

if __name__ == "__main__":
    print("🚀 Starting Tavily-LangChain Flight Price Agent...")
    print("Make sure your .env file contains OPENAI_API_KEY and TAVILY_API_KEY")
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Agent stopped by user.")
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        print("Please check your API keys and try again.")
