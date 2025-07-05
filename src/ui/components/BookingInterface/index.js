import React, { useState, useEffect } from 'react';
import flightDataService from '../../services/flightDataService.js';
import './styles.css';

const BookingInterface = ({ filters }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [bookingStatus, setBookingStatus] = useState(null);
  const [flights, setFlights] = useState([]);

  // Fetch flights from API
  useEffect(() => {
    const fetchFlights = async () => {
      try {
        setLoading(true);
        setError(null);
        
        let flightData;
        if (filters && (filters.from || filters.to || filters.maxPrice)) {
          // Only fetch flights when user has provided search criteria
          flightData = await flightDataService.searchFlights(filters);
        } else {
          // Don't show any flights initially - wait for user to search
          flightData = [];
        }
        
        setFlights(flightData);
      } catch (err) {
        console.error('Error fetching flights:', err);
        setError('Failed to load flight data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchFlights();
  }, [filters]);

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
      <h2>
        {filters && (filters.from || filters.to || filters.maxPrice) 
          ? `Available Flights (${filteredFlights.length})` 
          : 'Search for Flights'
        }
      </h2>
      
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
        {!filters || (!filters.from && !filters.to && !filters.maxPrice) ? (
          <div className="no-flights">
            <p>👋 Welcome to AirReserve!</p>
            <p>Use the search form above to find available flights.</p>
            <p>We have data for routes like:</p>
            <ul style={{ textAlign: 'left', maxWidth: '300px', margin: '0 auto' }}>
              <li>Vancouver to Toronto</li>
              <li>Toronto to Ottawa</li>
              <li>Calgary to Edmonton</li>
              <li>Ottawa to Montreal</li>
            </ul>
          </div>
        ) : filteredFlights.length > 0 ? (
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
