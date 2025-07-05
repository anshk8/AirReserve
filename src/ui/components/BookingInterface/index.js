import React, { useState, useEffect, useRef } from 'react';
import flightDataService from '../../services/flightDataService.js';
import './styles.css';

const BookingInterface = ({ filters }) => {
  const [loading, setLoading] = useState(true);
  const [backgroundLoading, setBackgroundLoading] = useState(false);
  const [error, setError] = useState(null);
  const [bookingStatus, setBookingStatus] = useState(null);
  const [flights, setFlights] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [autoRefresh, setAutoRefresh] = useState(true);
  const intervalRef = useRef(null);

  // Fetch flights from API
  const fetchFlights = async (showLoading = true, isBackground = false) => {
    try {
      if (showLoading) setLoading(true);
      if (isBackground) setBackgroundLoading(true);
      setError(null);
      
      let flightData;
      if (filters && (filters.from || filters.to || filters.maxPrice)) {
        // Apply filters when user has provided search criteria
        flightData = await flightDataService.searchFlights(filters);
      } else {
        // Show all flights initially
        flightData = await flightDataService.getAllFlights();
      }
      
      setFlights(flightData);
      setLastUpdated(new Date());
    } catch (err) {
      console.error('Error fetching flights:', err);
      setError('Failed to load flight data. Please try again later.');
    } finally {
      if (showLoading) setLoading(false);
      if (isBackground) setBackgroundLoading(false);
    }
  };

  // Initial fetch
  useEffect(() => {
    fetchFlights();
  }, [filters]);

  // Auto-refresh functionality
  useEffect(() => {
    if (autoRefresh) {
      // Set up polling every 10 seconds
      intervalRef.current = setInterval(() => {
        fetchFlights(false, true); // Background refresh with subtle indicator
      }, 10000);
    } else {
      // Clear interval if auto-refresh is disabled
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }

    // Cleanup interval on component unmount
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [autoRefresh, filters]);

  // Toggle auto-refresh
  const toggleAutoRefresh = () => {
    setAutoRefresh(prev => !prev);
  };

  // Manual refresh
  const handleManualRefresh = () => {
    fetchFlights();
  };

  // Apply filters to flights
  const filteredFlights = flights;


  const handleBookNow = (flightId) => {
    // In a real app, this would make an API call to book the flight
    console.log(`Booking flight with ID: ${flightId}`);
    setBookingStatus({ type: 'success', message: 'Flight booked successfully! '});
    
    // Clear the success message after 3 seconds
    setTimeout(() => {
      setBookingStatus(null);
    }, 3000);
  };

  const formatDate = (dateString) => {
    const options = { weekday: 'short', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  const calculateDuration = (departure, arrival) => {
    const diffMs = new Date(arrival) - new Date(departure);
    const diffMins = Math.floor(diffMs / 60000);
    const hours = Math.floor(diffMins / 60);
    const mins = diffMins % 60;
    return `${hours}h ${mins}m`;
  };

  const formatDateTime = (dateTimeString) => {
    const options = { 
      weekday: 'short', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    };
    return new Date(dateTimeString).toLocaleString('en-US', options);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading available flights...</p>
      </div>
    );
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="booking-interface">
      <div className="interface-header">
        <h2>Available Flights {filters && (filters.from || filters.to || filters.maxPrice) && `(${filteredFlights.length})`}</h2>
        
        {/* Auto-refresh controls */}
        <div className="refresh-controls">
          <div className="last-updated">
            Last updated: {lastUpdated.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
            {backgroundLoading && <span className="updating-indicator"> • Updating...</span>}
          </div>
          <div className="refresh-buttons">
            <button 
              className={`auto-refresh-toggle ${autoRefresh ? 'active' : ''}`}
              onClick={toggleAutoRefresh}
              title={autoRefresh ? 'Disable auto-refresh' : 'Enable auto-refresh'}
            >
              {autoRefresh ? '🔄 Auto ON' : '⏸️ Auto OFF'}
            </button>
            <button 
              className="manual-refresh"
              onClick={handleManualRefresh}
              disabled={loading || backgroundLoading}
              title="Refresh now"
            >
              {backgroundLoading ? '⏳' : '🔄'} Refresh
            </button>
          </div>
        </div>
      </div>
      
      {bookingStatus && (
        <div className={`booking-status ${bookingStatus.type}`}>
          {bookingStatus.message}
        </div>
      )}
      
      {/* Animated airplane icons */}
      {!loading && !error && filteredFlights.length > 0 && (
        <>
          <div className="airplane-icon">✈</div>
          <div className="airplane-icon">✈</div>
          <div className="airplane-icon">✈</div>
        </>
      )}
      
      <div className="flights-container">
        {filteredFlights.length > 0 ? (
          filteredFlights.map((flight) => (
            <div key={flight.id} className="flight-card">
              <div className="flight-header">
                <h3>{flight.airline}</h3>
                <span className="flight-number">{flight.flightNumber}</span>
              </div>
              
              <div className="flight-details">
                <div className="flight-route">
                  <div className="airport">
                    <span className="city">{flight.origin}</span>
                    <span className="time">
                      {new Date(flight.departureTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  
                  <div className="flight-path">
                    <div className="path-line"></div>
                    <div className="airplane-icon">✈</div>
                  </div>
                  
                  <div className="airport">
                    <span className="city">{flight.destination}</span>
                    <span className="time">
                      {new Date(flight.arrivalTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>
                
                <div className="flight-info">
                  <div className="info-item">
                    <span className="label">Date: </span>
                    <span>{formatDate(flight.departureTime)}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Duration: </span>
                    <span>{calculateDuration(flight.departureTime, flight.arrivalTime)}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Seats: </span>
                    <span className={`seats-${flight.seatsAvailable > 5 ? 'high' : 'low'}`}>
                      {flight.seatsAvailable} {flight.seatsAvailable === 1 ? 'seat' : 'seats'} left
                    </span>
                  </div>
                </div>
                
                <div className="flight-price">
                  <div className="price">${flight.price.toFixed(2)}</div>
                  <button 
                    className="book-button"
                    onClick={() => handleBookNow(flight.id)}
                    disabled={flight.seatsAvailable === 0}
                  >
                    {flight.seatsAvailable > 0 ? 'Book Now' : 'Sold Out'}
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="no-flights">
            <p>No flights found matching your criteria. Try adjusting your search.</p>
            {filters && (
              <button 
                className="clear-filters"
                onClick={() => {
                  // Clear filters by calling the parent component's filter reset
                  if (typeof filters.onClear === 'function') {
                    filters.onClear();
                  }
                }}
              >
                Clear Filters
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default BookingInterface;
