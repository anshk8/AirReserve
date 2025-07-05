# Issue 3: LangChain Asynchronous Agent for Price Monitoring

## Project Context
- **Location**: `src/agent/` (LangChain agent components)
- **Purpose**: Develop an asynchronous agent using LangChain that monitors flight price data for drops below user-defined thresholds and sends notifications
- **Status**: Tavily API integration completed in Issue #2 ✅

## Current State Analysis

### About Issue #2 Integration
The Tavily price tracker tool in `src/agent/tools/tavily_price_tracker.py` is now complete and:
- Fetches flight price data using Tavily API
- Stores data in `src/data/flight_prices.json`
- Returns formatted price information for LangChain integration
- Handles API rate limits and data parsing challenges

### Requirements Overview
- Create an asynchronous LangChain agent that runs in the background
- Monitor flight prices from the JSON data file
- Send notifications when prices drop below user-defined thresholds
- Implement proper error handling and continuous operation
- Test with simulated price drops

## Task List

### 1. Set Up LangChain Environment
- [x] Verify LangChain installation from Issue #1
- [x] Install additional LangChain dependencies:
  - `langchain-community` for async support
  - `asyncio` for asynchronous operations
  - Any other required packages
- [x] Test basic LangChain functionality:
  - Import and print version
  - Verify async capabilities work
- [x] Create virtual environment if needed
- [x] Create and run async test script to verify environment
- [x] Commit environment setup and test script

### 2. Create Price Monitoring Script
- [x] Create `src/agent/langchain_notifier.py`
- [x] Implement basic JSON file reading:
  ```python
  import json
  import time
  
  with open("src/data/flight_prices.json", "r") as f:
      prices = json.load(f)
  ```
- [x] Add user-defined threshold parameter (default: $200)
- [x] Implement basic monitoring loop:
  ```python
  threshold = 200  # User-defined threshold
  while True:
      for flight in prices:
          if flight["price"] < threshold:
              print(f"Price drop! {flight['airline']} to {flight['destination']} at ${flight['price']}")
      time.sleep(60)  # Check every minute
  ```
- [x] Add error handling for file read failures

### 3. Implement Asynchronous Logic
- [x] Convert monitoring loop to async function:
  ```python
  import asyncio
  
  async def monitor_prices(prices, threshold):
      while True:
          for flight in prices:
              if flight["price"] < threshold:
                  await send_notification(flight)
          await asyncio.sleep(60)
  ```
- [x] Create async notification function:
  ```python
  async def send_notification(flight):
      print(f"Alert: Price drop for {flight['airline']} to {flight['destination']} at ${flight['price']}")
  ```
- [x] Integrate with LangChain's agent framework
- [x] Implement background execution capability

### 4. Enhanced Notification System
- [x] Add multiple notification channels:
  - Console logging (basic)
  - Discord webhook (optional)
  - Email notifications (optional)
- [x] Create notification configuration system
- [x] Implement notification throttling to prevent spam
- [x] Add notification history tracking

### 5. Real-time Data Integration
- [x] Investigate Tavily API streaming options
- [x] Implement real-time price updates if available
- [x] Add data refresh mechanism for JSON file
- [x] Handle concurrent file access safely

### 6. Testing & Validation
- [x] Test with sample data:
  - Manually edit `flight_prices.json` to simulate price drops
  - Set prices below threshold (e.g., $180)
  - Verify agent detects drops and sends notifications
- [x] Test error scenarios:
  - Corrupted JSON file
  - Missing file
  - Network failures
  - API rate limit exceeded
- [x] Verify continuous operation without crashes
- [x] Test notification delivery (console, Discord if configured)

### 7. Performance Optimization
- [x] Optimize sleep intervals (not too short, not too long)
- [x] Implement efficient data loading (avoid reading entire file each time)
- [x] Add memory usage monitoring
- [x] Implement graceful shutdown handling

### 8. Documentation & Configuration
- [x] Add comprehensive code comments explaining async logic and performance features
- [x] Document configuration file options (thresholds, notification, performance)
- [x] Document performance considerations and sleep interval tuning
- [x] Create setup instructions for Discord webhook (if implemented)
- [x] Add troubleshooting guide for common issues
- [x] Review and update README with usage and configuration instructions

#### Task 8 Subtasks
- [x] Add/expand code comments in all major modules (`langchain_notifier.py`, `performance_optimizer.py`, etc.)
- [x] Write or update documentation for `config/notification_config.json` (all sections)
- [x] Add a section to the README on performance tuning and monitoring
- [x] Provide step-by-step Discord webhook setup instructions
- [x] Add a troubleshooting section to the README for common errors (e.g., missing config, Discord errors, memory issues)
- [x] Ensure all documentation is clear, up-to-date, and user-friendly

## Technical Notes

### File Structure
```
src/
├── agent/
│   ├── tools/
│   │   └── tavily_price_tracker.py (from Issue #2)
│   └── langchain_notifier.py (new)
├── data/
│   └── flight_prices.json (from Issue #2)
└── config/
    └── notification_config.json (new, optional)
```

### Dependencies to Install
- `langchain` (from Issue #1)
- `langchain-community` (for async support)
- `asyncio` (built-in)
- `aiofiles` (for async file operations)
- `discord.py` (optional, for Discord notifications)
- `psutil` (for memory monitoring)

### Configuration Parameters
- `threshold`: User-defined price threshold (default: $200)
- `check_interval`: How often to check prices (default: 60 seconds)
- `notification_channels`: List of enabled notification methods
- `discord_webhook_url`: Discord webhook URL (optional)
- `performance`: Performance optimization settings (adaptive sleep, memory threshold, etc.)

## Questions to Address

1. **Real-time vs Batch Updates**: Should we implement real-time streaming from Tavily API or stick with periodic JSON file checks?
2. **Notification Channels**: Which notification methods should be prioritized (console, Discord, email)?
3. **Performance**: What's the optimal check interval to balance responsiveness with API rate limits?
4. **Data Persistence**: Should we implement a database for notification history or keep it simple with JSON?

## Next Steps
1. 🎯 Task 1: Set up LangChain environment - START HERE
2. 📝 Task 2: Create basic price monitoring script
3. ⚡ Task 3: Implement asynchronous logic
4. 🔔 Task 4: Add notification system
5. 🔄 Task 5: Integrate real-time updates
6. 🧪 Task 6: Comprehensive testing
7. ⚙️ Task 7: Performance optimization
8. 📚 Task 8: Documentation and configuration

## Success Criteria
- [ ] Agent runs continuously in background without crashes
- [ ] Detects price drops below threshold and sends notifications
- [ ] Handles errors gracefully and continues operation
- [ ] Configurable thresholds and notification settings
- [ ] Well-documented code with clear async logic explanations
- [ ] Tested with simulated price drops and various error conditions 

## How to Run and Test the LangChain Agent (For Teammates)

1. **Clone the Repository**
   - `git clone <repo-url>`
   - `cd AirReserve`

2. **Set Up Python Virtual Environment**
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`

3. **Install Python Dependencies**
   - `pip install --upgrade pip`
   - `pip install -r requirements.txt`

4. **Install Node.js Dependencies** (if needed)
   - `npm install`

5. **Set Up Environment Variables**
   - Copy the `.env` template (if provided) or create a `.env` file in the project root.
   - **Add your own API keys** for Tavily, OpenAI, Firebase, etc. (Do NOT share or commit real API keys.)
   - Example `.env` variables:
     ```env
     TAVILY_API_KEY=your_own_tavily_key
     OPENAI_API_KEY=your_own_openai_key
     FIREBASE_PROJECT_ID=your_project_id
     # ...other keys as needed
     ```

6. **Configure Notifications**
   - Edit `config/notification_config.json` to set your price threshold, check interval, and notification channels.
   - To enable Discord notifications, add your Discord webhook URL to `discord_webhook_url`.
   - Example:
     ```json
     {
       "threshold": 200,
       "check_interval": 60,
       "notification_channels": ["console", "discord"],
       "discord_webhook_url": "https://discord.com/api/webhooks/your_webhook_here"
     }
     ```

7. **Verify Setup**
   - Run the verification script:
     `python setup/test_setup.py`
   - All checks should pass (6/6 tests passed).

8. **Run the LangChain Agent Tests**
   - To test the real-time data manager and notification system:
     `python test_issue3_langchain_agent.py`
   - Check the output for price drop notifications and configuration validation.
   - If Discord is configured, check your Discord channel for notifications.

9. **Safe Sharing**
   - This task list and the codebase are safe to share publicly **as long as you do NOT include your real API keys or Discord webhook**.
   - `.env` and sensitive config values should be in `.gitignore` and never committed.
   - Each teammate should use their own API keys and webhook for testing and development.

---

*If you have any issues, check the troubleshooting section in `setup/README.md` or ask in the team chat!* 