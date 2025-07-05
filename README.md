# AirReserve

An intelligent flight booking and price tracking application that combines real-time web crawling and ambient AI agents to provide a seamless and affordable travel planning experience for everyone.

## Overview

AirReserve is a flight search and booking platform that uses AI-based solutions to provide users with real-time flight data, intelligent price monitoring, and an intuitive booking interface.

## Key Features

### Intelligent Flight Search
- **Real-time data crawling** using Tavily API to fetch live flight prices from multiple sources
- **Natural language processing** for intuitive search queries
- **Smart filtering and sorting** based on user preferences
- **Price comparison** across multiple airlines and booking platforms

### Powered by Ambient AI Agents
- **Background monitoring** ambient agents built with Langchain
- **Automated price tracking** without user intervention
- **Intelligent notifications** when price thresholds are met
- **Continuous learning** from user behavior and preferences

### Advanced Integrations
- **Firebase backend** for real-time data synchronization
- **MCP (Media Control Protocol)** integration for enhanced agent communication
- **External API orchestration** for comprehensive data aggregation

## Technology Stack

### Frontend
- Modern React-based UI framework built with Windsurf

### Backend & AI
- **Python 3.8+** - Core backend language
- **FastAPI** - High-performance web framework
- **LangChain** - AI agent framework and orchestration
- **LangGraph** - Advanced agent workflow management
- **Tavily API** - Real-time web crawling and data extraction

### Data & Infrastructure
- **Firebase** - Real-time database and authentication
- **MCP Protocol** - Media Control Protocol for agent communication
- **Node.js** - JavaScript runtime for build tools
- **Express.js** - Web server framework

### Development Tools
- **Windsurf** - Workflow orchestration and UI development
- **Cursor** - AI-powered backend development
- **Babel** - JavaScript transpilation
- **Jest** - Testing framework

## Architecture

### Ambient AI Agent System
The application features a sophisticated ambient agent that runs in the background, continuously monitoring flight prices and market conditions. This agent:
- Operates autonomously without constant user input
- Learns from user preferences and search patterns
- Provides proactive notifications and recommendations
- Maintains context across multiple user sessions

### Real-time Data Pipeline
```
Tavily API → Data Processing → LangChain Agent → Firebase → React UI
```

### MCP Integration
The Media Control Protocol integration enables:
- Seamless communication between different agent components
- Standardized data exchange protocols
- Enhanced reliability and error handling
- Scalable agent architecture

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- Git version control
- API keys for external services

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/anshk8/AirReserve.git
cd AirReserve
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Node.js dependencies**
```bash
npm install
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys:
# - TAVILY_API_KEY
# - OPENAI_API_KEY
# - FIREBASE_CONFIG
```

5. **Start the development servers**
```bash
# Backend server
uvicorn src.main:app --reload

# Frontend development server
npm run dev
```

### Production Deployment
```bash
# Build frontend assets
npm run build

# Start production server
npm start
```

## Project Structure

```
AirReserve/
├── src/
│   ├── agent/              # AI agent components
│   │   ├── tools/          # LangChain tools and utilities
│   │   └── workflows/      # Agent workflow definitions
│   ├── api/                # FastAPI backend endpoints
│   ├── ui/                 # React frontend components
│   │   ├── components/     # Reusable UI components
│   │   └── styles/         # CSS styling
│   └── utils/              # Shared utilities
├── config/                 # Configuration files
├── data/                   # Data storage and cache
├── docs/                   # Documentation
├── scripts/                # Build and deployment scripts
└── tests/                  # Test suites
```

## Key Capabilities

### Web Crawling & Data Enrichment
- Utilizes Tavily's advanced web crawling API to gather real-time flight data
- Processes and enriches data from multiple airline websites
- Maintains data freshness through continuous background updates
- Handles rate limiting and API optimization automatically

### Intelligent Agent Workflows
- Implements complex decision-making processes using LangGraph
- Manages multi-step flight search and booking workflows
- Provides contextual recommendations based on user history
- Handles error recovery and fallback strategies

### Secure Data Handling
- Implements secure API key management
- Uses Firebase security rules for data protection
- Follows best practices for credential storage
- Provides audit trails for all data access

### Voice Interface Integration
- Supports voice-based flight searches and bookings
- Implements secure voice data processing
- Provides hands-free interaction capabilities
- Maintains conversation context across voice sessions

## Usage Examples

### Basic Flight Search
```python
# Search for flights using natural language
result = agent.search_flights(
    query="Find flights from Toronto to Vancouver next Friday",
    max_price=500,
    preferences={"airline": "Air Canada", "stops": "direct"}
)
```

### Price Monitoring Setup
```python
# Set up ambient price monitoring
monitor = agent.create_price_monitor(
    route="YYZ-YVR",
    target_price=300,
    notification_method="discord"
)
```

### Voice Interface
```python
# Process voice commands
response = voice_agent.process_command(
    audio_input=voice_data,
    user_context=current_session
)
```

## API Documentation

The application exposes RESTful APIs for:
- Flight search and booking operations
- User preference management
- Price monitoring configuration
- Real-time data access

Detailed API documentation is available at `/docs` when running the development server.

## Contributing

We welcome contributions to AirReserve! Please see our contributing guidelines for:
- Code style and standards
- Testing requirements
- Pull request process
- Issue reporting

## Security

- All API keys are stored securely in environment variables
- Firebase security rules protect user data
- Regular security audits and dependency updates
- Secure communication protocols throughout the stack

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Tavily for providing advanced web crawling capabilities
- LangChain for the powerful agent framework
- Firebase for reliable backend infrastructure
- The open-source community for various tools and libraries

---

**Note**: This application demonstrates advanced integration of multiple AI technologies and represents a comprehensive approach to modern web application development with ambient AI capabilities.