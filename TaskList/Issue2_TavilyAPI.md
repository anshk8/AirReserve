# Issue 2: Tavily API Integration for Price Tracking

## Project Context
- **Location**: `src/agent/tools/` (as requested by teammate)
- **Purpose**: Integrate Tavily API to fetch flight price data for the LangChain ambient agent and Windsurf UI
- **Status**: API access already set up ✅

## Current State Analysis

### About `add_tool.py`
The `add_tool.py` file in `src/agent/tools/` is **NOT** part of our issue. It's a simple example tool that:
- Adds two integers from a comma-separated string input
- Returns the sum as a string
- Appears to be a template/example for how to create LangChain tools

### Teammate's Requirements
- **Location**: Use `src/agent/tools/` instead of `src/data/`
- **Parameter Structure**: Use a single object parameter with `{TO: str, FROM: str, maxPrice: int}` to avoid the "only one param" limitation
- **Purpose**: This will be used by the LangChain ambient agent for notifications

## Task List

### 1. Create Tavily Price Tracker Tool
- [*] Create `src/agent/tools/tavily_price_tracker.py`
- [*] Import required dependencies:
  - `os` for environment variables
  - `requests` for API calls
  - `json` for data handling
  - `from langchain.tools import tool` for LangChain integration
- [*] Implement the tool function with single object parameter:
  ```python
  @tool
  def tavily_price_tracker(params: dict) -> str:
      """
      Fetch flight prices using Tavily API
      params: {TO: str, FROM: str, maxPrice: int}
      """
  ```

### 2. API Integration Implementation
- [*] Load environment variables for Tavily API key
- [*] Implement Tavily API request logic:
  - Use web-crawl endpoint: `https://api.tavily.com/web-crawl`
  - Construct query: "flight prices {FROM} to {TO}"
  - Handle API response and error cases
- [*] Parse flight price data from response
- [*] Filter results based on `maxPrice` parameter
- [*] Return formatted price information

### 3. Data Storage
- [*] Create local JSON storage in `data/flight_prices.json`
- [*] Implement data structure with fields:
  - `price`: float
  - `airline`: str
  - `departure`: str
  - `destination`: str
  - `timestamp`: str
- [*] Add error handling for file operations

### 4. Testing & Validation
- [*] Test with sample routes:
  - Toronto → Ottawa
  - Ottawa → Montreal
  - Add 1-2 more routes
- [*] Verify data is fetched and stored correctly
- [*] Test error handling (API failures, invalid parameters)
- [*] Confirm `maxPrice` filtering works
- [*] Add success/error logging

### 5. Documentation
- [*] Add comprehensive code comments in `src/agent/tools/tavily_price_tracker.py`
- [*] Documented API rate limits and challenges below
- [*] Updated this task list with completion status
- [*] Noted deviations from original requirements

#### Documentation Notes
- **Code Comments**: All major functions and logic in `tavily_price_tracker.py` are now clearly commented for maintainability.
- **API Rate Limits/Challenges**: Tavily API has 1000 free credits. Some flight data is difficult to parse due to inconsistent formatting from different sources. Only price and airline are reliably extracted; other fields are set to 'Unknown'.
- **Deviations**: Full flight details (route, date/time, duration) could not be reliably parsed due to data variability. Only the top 3 lowest-price flights are returned per search.

## Technical Notes

### Parameter Structure
Based on teammate's feedback, the tool should accept:
```python
{
    "TO": "Ottawa",
    "FROM": "Toronto", 
    "maxPrice": 500
}
```

### File Structure
```
src/
├── agent/
│   └── tools/
│       ├── add_tool.py (existing, not related)
│       └── tavily_price_tracker.py (new)
└── data/
    └── flight_prices.json (new)
```

### Dependencies to Install
- `requests` (likely already installed)
- `python-dotenv` (for environment variables)
- `beautifulsoup4` (if HTML parsing needed)

## Questions Answered

1. **Is `add_tool.py` part of our issue?** 
   - **No**, it's an unrelated example tool for adding integers

2. **Is `src/agent/tools/` better than `src/data/`?**
   - **Yes**, according to your teammate's preference and the fact that this will be used by the LangChain ambient agent

3. **Parameter structure requirement?**
   - Use single object parameter: `{TO: str, FROM: str, maxPrice: int}` to avoid the "only one param" limitation

## Next Steps
1. ✅ Task 1: Create the tool file - COMPLETED
2. ✅ Task 2: Implement basic API integration - COMPLETED  
3. ✅ Task 3: Add data storage functionality - COMPLETED
4. 🎯 Task 4: Test with sample routes - NEXT
5. 📝 Task 5: Document any issues or challenges encountered 

## How to Run This Project (For Teammates)

1. **Clone the Repository**
   - `git clone <repo-url>`
   - `cd AirReserve`

2. **Set Up Python Virtual Environment**
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`

3. **Install Python Dependencies**
   - `pip install --upgrade pip`
   - `pip install -r requirements.txt`

4. **Install Node.js Dependencies**
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

6. **Verify Setup**
   - Run the verification script:
     `python setup/test_setup.py`
   - All checks should pass (6/6 tests passed).

7. **Run Tests**
   - To test the Tavily price tracker tool:
     `python test_tavily_price_tracker.py`
   - Check the output and generated files in the `data/` directory.

8. **Safe Sharing**
   - This task list and the codebase are safe to share publicly **as long as you do NOT include your real API keys**.
   - `.env` should be in `.gitignore` and never committed.
   - Each teammate should use their own API keys for testing and development.

---

*If you have any issues, check the troubleshooting section in `setup/README.md` or ask in the team chat!* 