
# AIRRESERVE HACKATHON DEMO SCRIPT
# Demo Time: 6:30 PM, Saturday July 5, 2025

## 1. INTRODUCTION (2 minutes)
"Hi everyone! We're team AirReserve (Nolan, Derek, Nick, Ansh) and we've built an 
Automated Flight Price Tracker and Booker that integrates Tavily API, LangChain, 
Windsurf UI, and Firebase. Let me show you how it works!"

## 2. DEMO FLOW (8 minutes)

### Step 1: Show the UI (2 minutes)
- Open browser to http://localhost:3001
- Show the beautiful Windsurf UI with real flight data
- Demonstrate search functionality (Toronto to Vancouver, max $500)
- Point out: "This data comes from our Tavily API integration"

### Step 2: Show Real-time Data (2 minutes)
- Open terminal and show the data files: ls data/
- Show a flight data file: cat data/flight_prices_Toronto_Vancouver.json
- Point out: "This is real flight data fetched by our Tavily integration"

### Step 3: Demonstrate LangChain Agent (2 minutes)
- Run: python test_notifications.py
- Show console output with price drop notifications
- Point out: "Our LangChain agent monitors prices 24/7 and sends notifications"

### Step 4: Show Discord Integration (1 minute)
- Open Discord channel
- Show notifications appearing in real-time
- Point out: "Users get instant alerts when prices drop below their threshold"

### Step 5: Demonstrate Booking (1 minute)
- Go back to UI
- Click "Book Now" on a flight
- Show success message
- Point out: "This simulates the booking workflow"

## 3. TECHNICAL HIGHLIGHTS (2 minutes)

### Tavily API Integration
- Real-time flight price scraping
- Intelligent data parsing and filtering
- Local JSON storage for persistence

### LangChain Ambient Agent
- Asynchronous price monitoring
- Smart notification throttling
- Performance optimization

### Windsurf UI
- Modern, responsive design
- Real-time data integration
- Beautiful animations and UX

### Firebase Integration
- Secure data storage
- Real-time database updates
- Scalable architecture

## 4. PRIZE ALIGNMENT (1 minute)

### Best Use of Tavily API
- Real-time flight price scraping
- Intelligent data processing
- Comprehensive integration

### Best Ambient/Async Agent
- 24/7 background monitoring
- Smart notification system
- Performance optimized

### Best Use of Windsurf
- Modern, beautiful UI
- Real-time data integration
- Excellent user experience

### Most Impactful Project
- Solves real travel problem
- Saves users money
- Easy to use interface

## 5. CLOSING (1 minute)
"AirReserve demonstrates how modern AI tools can work together to solve real problems. 
We've integrated Tavily's powerful web scraping, LangChain's intelligent agents, 
Windsurf's beautiful UI, and Firebase's reliable storage to create a complete 
flight booking solution. Thank you!"

## DEMO COMMANDS TO RUN:

# Terminal 1: Start the UI server
npm run dev

# Terminal 2: Test notifications
python test_notifications.py

# Terminal 3: Force a notification (if needed)
python force_notification.py

# Terminal 4: Monitor logs
tail -f data/notification_history.json
