# Firebase Monitoring System Setup

## Overview
This system automatically monitors your Firebase database for new flight search entries and triggers Tavily API calls when new entries are detected.

## Components Created

### 1. Firebase Listener (`src/agent/firebase_listener.py`)
- **Purpose**: Monitors Firebase Realtime Database for new flight search entries
- **Features**:
  - Polls Firebase every 5 seconds (configurable)
  - Detects new entries and processes them automatically
  - Calls Tavily API for flight price searches
  - Saves processing results back to Firebase
  - Thread-safe background operation

### 2. Updated MCP Server (`src/agent/MCPLangChainServer.py`)
- **New Tools Added**:
  - `start_monitoring_firebase()` - Start monitoring service
  - `stop_monitoring_firebase()` - Stop monitoring service  
  - `get_monitoring_status()` - Get current monitoring status
  - `search_flight_prices()` - Manual Tavily API calls

### 3. Monitoring Service Script (`start_monitoring.py`)
- **Purpose**: Standalone script to start the monitoring service
- **Usage**: `python start_monitoring.py [poll_interval]`
- **Features**: Easy start/stop with Ctrl+C

### 4. Test Suite (`test_monitoring_system.py`)
- **Purpose**: Comprehensive testing of the entire system
- **Tests**:
  - Environment variables setup
  - Firebase database connectivity
  - Tavily API connectivity
  - End-to-end monitoring workflow

## How It Works

1. **User adds flight search via UI** → Firebase database
2. **Firebase Listener detects new entry** → Extracts flight details
3. **Tavily API called automatically** → Searches for flight prices
4. **Results saved back to Firebase** → Under `processed_searches` node
5. **Console logging** → Shows all activity in real-time

## Quick Start

### Step 1: Test the System
```bash
python test_monitoring_system.py
```

### Step 2: Start Monitoring
```bash
python start_monitoring.py
```

### Step 3: Add Flight Searches
- Use your UI to add flight searches
- Watch the console for automatic processing
- Check Firebase for results under `processed_searches`

## Environment Variables Required

Make sure these are set in your `.env` file:
```
FIREBASE_DATABASE_URL=https://your-project-default-rtdb.firebaseio.com/
TAVILY_API_KEY=your_tavily_api_key_here
```

## MCP Server Integration

You can also control monitoring through MCP tools:

```python
# Start monitoring
start_monitoring_firebase(poll_interval=5)

# Check status
get_monitoring_status()

# Stop monitoring
stop_monitoring_firebase()

# Manual price search
search_flight_prices(from_city="Toronto", to_city="Paris", max_price="800")
```

## Firebase Database Structure

### Input (from UI):
```json
{
  "flight_searches": {
    "record_id": {
      "to": "PARIS",
      "from": "TORONTO", 
      "maxPrice": 800,
      "userId": "default",
      "timestamp": "2025-01-05T10:30:00Z"
    }
  }
}
```

### Output (from monitoring):
```json
{
  "processed_searches": {
    "processing_id": {
      "original_search_id": "record_id",
      "tavily_result": "✅ Found 3 flights from TORONTO to PARIS under $800...",
      "processed_at": "2025-01-05T10:30:05Z",
      "original_search": { ... }
    }
  }
}
```

## Troubleshooting

### Common Issues:
1. **"Firebase URL not configured"** - Check your `.env` file
2. **"Tavily API key not found"** - Verify TAVILY_API_KEY is set
3. **"No new entries detected"** - UI may not be writing to Firebase correctly
4. **"Import errors"** - Make sure you're running from the correct directory

### Debug Steps:
1. Run the test suite first: `python test_monitoring_system.py`
2. Check console output for error messages
3. Verify Firebase database has new entries
4. Test Tavily API manually with `search_flight_prices()`

## Customization

### Change Poll Interval:
```bash
python start_monitoring.py 10  # Check every 10 seconds
```

### Modify Processing Logic:
Edit `_process_flight_search()` in `firebase_listener.py` to add:
- Email notifications
- Slack alerts
- Custom filtering logic
- Different API calls

### Add More Data:
Extend the Firebase structure to include:
- Departure dates
- Return dates
- Passenger count
- Airline preferences
