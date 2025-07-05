import React, { useState } from 'react';
import BookingInterface from './components/BookingInterface/index.js';
import configDatabase from './services/firebaseService.js';
import { getDatabase, ref, push, set, remove } from 'firebase/database';
import './App.css';

// Background component
const Background = () => {
  return (
    <div className="background">
      <div className="gradient-bg"></div>
    </div>
  );
};

function App() {
  const [searchParams, setSearchParams] = useState({
    from: '',
    to: '',
    maxPrice: ''
  });

  const [filters, setFilters] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [messageSent, setMessageSent] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSearchParams(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage(null);

    try {
      // Initialize Firebase database
      const database = getDatabase(configDatabase);
      const referenceDatabase = ref(database, "flight_searches");

      // Clear the entire flight_searches database first
      await remove(referenceDatabase);
      console.log('Previous search data cleared from Firebase');

      // Push the new search data to Firebase
      const pushMessageRef = push(referenceDatabase);
      await set(pushMessageRef, {
        FROM: searchParams.from,
        TO: searchParams.to,
        MAX_PRICE: searchParams.maxPrice || null,
        TIMESTAMP: new Date().toISOString(),
        SEARCH_ID: pushMessageRef.key
      });

      console.log('New search data saved to Firebase successfully');
      
      setMessage({ type: 'success', text: `Searching flights from ${searchParams.from} to ${searchParams.to}` });
      
      // Apply filters for flight search
      setFilters({
        from: searchParams.from.toUpperCase(),
        to: searchParams.to.toUpperCase(),
        maxPrice: searchParams.maxPrice ? parseFloat(searchParams.maxPrice) : null
      });

      // Clear the form fields after successful submission
      setSearchParams({
        from: '',
        to: '',
        maxPrice: ''
      });

    } catch (error) {
      console.error('Error saving to Firebase:', error);
      setMessage({ type: 'error', text: `Error: ${error.message}` });
    } finally {
      setIsLoading(false);
      
      // Clear message after 5 seconds
      setTimeout(() => {
        setMessage(null);
      }, 5000);
    }
  };

  const clearFilters = () => {
    setFilters(null);
    setMessage({ type: 'info', text: 'Filters cleared. Showing all available flights.' });
    
    // Clear message after 3 seconds
    setTimeout(() => {
      setMessage(null);
    }, 3000);
  };





  return (
    <div className="app">
      <Background />
      <header className="app-header">
        <div className="header-content">
          <h1>AirReserve</h1>
          <p className="subtitle">Your next journey starts here</p>
          <div className="scroll-indicator">
            <span>Scroll to explore</span>
            <div className="arrow"></div>
          </div>
        </div>
        
        <form onSubmit={handleSearch} className="search-form">
          {message && (
            <div className={`message ${message.type}`}>
              {message.text}
            </div>
          )}
          
          <div className="form-group">
            <label htmlFor="from">From:</label>
            <input
              type="text"
              id="from"
              name="from"
              value={searchParams.from}
              onChange={handleInputChange}
              placeholder="City or Airport Code"
              required
              disabled={isLoading}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="to">To:</label>
            <input
              type="text"
              id="to"
              name="to"
              value={searchParams.to}
              onChange={handleInputChange}
              placeholder="City or Airport Code"
              required
              disabled={isLoading}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="maxPrice">Max Price ($):</label>
            <input
              type="number"
              id="maxPrice"
              name="maxPrice"
              value={searchParams.maxPrice}
              onChange={handleInputChange}
              placeholder="Maximum price"
              min="0"
              step="0.01"
              disabled={isLoading}
            />
          </div>
          
          <button type="submit" className="search-button" disabled={isLoading}>
            {isLoading ? 'Saving & Searching...' : 'Search Flights'}
          </button>
        </form>
      </header>
      
      <main>
        <BookingInterface filters={{ ...filters, onClear: clearFilters }} />
      </main>
      
      <footer className="app-footer">
        <p>© 2025 AirReserve. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
