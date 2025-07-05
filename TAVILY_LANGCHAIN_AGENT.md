# Tavily-LangChain Flight Price Agent

## Overview

The Tavily-LangChain Flight Price Agent is an intelligent conversational AI that combines the power of LangChain's agent framework with Tavily's real-time web crawling capabilities to provide comprehensive flight price monitoring and analysis.

## Features

### 🔍 **Real-Time Flight Search**
- Uses Tavily API to crawl live flight price data from the web
- Searches multiple airlines and booking platforms
- Provides current market prices and availability

### 🤖 **Conversational AI Interface**
- Natural language interaction powered by OpenAI GPT
- Understands complex flight search queries
- Provides intelligent recommendations and insights

### 📊 **Price Monitoring & Alerts**
- Set up automated monitoring for specific routes
- Configure price thresholds for alerts
- Track price trends over time

### 💾 **Data Management**
- Saves flight data locally for analysis
- Maintains search history and price trends
- Provides data export and analysis tools

### 🔔 **Smart Notifications**
- Price drop alerts when flights fall below thresholds
- Trend analysis and booking recommendations
- Multiple notification channels (console, Discord, etc.)

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables**
   Create a `.env` file with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

3. **Create Data Directories**
   ```bash
   mkdir -p data/monitoring data/alerts
   ```

## Usage

### Command Line Interface

#### **Basic Usage**
```bash
python run_tavily_agent.py
```

#### **With Custom API Keys**
```bash
python run_tavily_agent.py --openai-key YOUR_KEY --tavily-key YOUR_KEY
```

#### **Test Mode**
```bash
python run_tavily_agent.py --test
```

### Interactive Commands

Once the agent is running, you can use natural language commands:

#### **Flight Search**
```
"Find flights from Toronto to Vancouver under $500"
"What are the cheapest flights from NYC to LA?"
"Search for flights from Montreal to Calgary"
```

#### **Price Monitoring**
```
"Monitor flights from Toronto to Ottawa, alert me if under $300"
"Start monitoring Vancouver to Toronto flights"
"Stop monitoring all flights"
```

#### **Data Analysis**
```
"Show me saved flight data"
"Analyze price trends for Toronto to Vancouver"
"What's the best time to book flights to Europe?"
```

#### **Price Alerts**
```
"Set a price alert for Montreal to Toronto flights at $250"
"Alert me when Vancouver to Calgary flights drop below $400"
```

## Testing

### **Comprehensive Test Suite**
```bash
python test_tavily_langchain_integration.py
```

### **Quick Test**
```bash
python test_tavily_langchain_integration.py --quick
```

### **Interactive Demo**
```bash
python test_tavily_langchain_integration.py --demo
```

## Architecture

### **Core Components**

1. **TavilyLangChainAgent**
   - Main agent class that orchestrates all functionality
   - Manages LangChain agent executor and tools
   - Handles conversation state and history

2. **LangChain Tools**
   - `tavily_search_flights`: Real-time flight price search
   - `start_flight_monitoring`: Begin monitoring a route
   - `stop_flight_monitoring`: Stop monitoring routes
   - `get_saved_flight_data`: Retrieve historical data
   - `analyze_price_trends`: Perform price trend analysis
   - `set_price_alert`: Configure price alerts

3. **Data Management**
   - Local JSON storage for flight data
   - Monitoring configuration management
   - Price alert system

### **Integration Points**

- **Tavily API**: Web crawling for real-time flight prices
- **OpenAI API**: Conversational AI and natural language processing
- **Real-Time Data Manager**: Caching and data refresh logic
- **Notification System**: Alert delivery and management

## Configuration

### **Environment Variables**
```env
# Required
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key

# Optional
DISCORD_WEBHOOK_URL=your_discord_webhook_url
```

### **Data Structure**

#### **Flight Data Format**
```json
{
  "searches": [
    {
      "search_timestamp": "2024-01-15T10:30:00",
      "from_city": "Toronto",
      "to_city": "Vancouver",
      "max_price": "500",
      "flights": [
        {
          "price": "450",
          "airline": "Air Canada",
          "departure": "YYZ",
          "destination": "YVR",
          "url": "booking_url"
        }
      ]
    }
  ]
}
```

#### **Monitoring Configuration**
```json
{
  "route": "Toronto to Vancouver",
  "threshold": 400,
  "started_at": "2024-01-15T10:30:00",
  "status": "active"
}
```

## API Integration

### **Tavily API**
- Endpoint: `https://api.tavily.com/search`
- Purpose: Real-time web crawling for flight prices
- Rate Limits: Varies by plan
- Response: Structured flight price data

### **OpenAI API**
- Model: GPT-3.5-turbo (configurable)
- Purpose: Natural language processing and conversation
- Temperature: 0.1 (for consistent responses)
- Max Tokens: Configurable per request

## Error Handling

The agent includes comprehensive error handling for:

- **API Rate Limits**: Automatic retry with backoff
- **Invalid Inputs**: Graceful error messages
- **Network Issues**: Timeout and connection error handling
- **Data Corruption**: Validation and recovery mechanisms
- **Missing Configuration**: Clear setup instructions

## Performance Considerations

- **Caching**: Local data storage reduces API calls
- **Rate Limiting**: Built-in delays prevent API abuse
- **Memory Management**: Efficient data structures and cleanup
- **Async Operations**: Non-blocking I/O for better responsiveness

## Troubleshooting

### **Common Issues**

1. **Missing API Keys**
   ```
   Error: OpenAI API key is required
   Solution: Set OPENAI_API_KEY in .env file
   ```

2. **Import Errors**
   ```
   Error: ModuleNotFoundError: No module named 'src'
   Solution: Run from project root directory
   ```

3. **Rate Limiting**
   ```
   Error: 429 Too Many Requests
   Solution: Wait and retry, check API quotas
   ```

4. **No Flight Data**
   ```
   Error: No flights found
   Solution: Try different cities or higher price limits
   ```

### **Debug Mode**

Enable verbose logging by setting:
```python
agent = TavilyLangChainAgent()
agent.agent_executor.verbose = True
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is part of the AirReserve flight monitoring system.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Run the test suite to identify problems
3. Review the logs for error details
4. Create an issue with reproduction steps

---

**Happy Flight Hunting! ✈️**
