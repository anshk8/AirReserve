import React, { useState, useEffect } from 'react';
import BookingInterface from './components/BookingInterface';
import FloatingIcons from './components/FloatingIcons';
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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSearchParams(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setFilters({
      from: searchParams.from.toUpperCase(),
      to: searchParams.to.toUpperCase(),
      maxPrice: searchParams.maxPrice ? parseFloat(searchParams.maxPrice) : null
    });
  };

  return (
    <div className="app">
      <Background />
      <FloatingIcons />
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
            />
          </div>
          
          <button type="submit" className="search-button">
            Search Flights
          </button>
        </form>
      </header>
      
      <main>
        <BookingInterface filters={filters} />
      </main>
      
      <footer className="app-footer">
        <p>© 2025 AirReserve. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
