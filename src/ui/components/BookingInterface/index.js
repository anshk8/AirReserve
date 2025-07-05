import React, { useState, useEffect } from 'react';
import './styles.css';

const BookingInterface = ({ filters }) => {
  const [flights, setFlights] = useState([]);
  const [filteredFlights, setFilteredFlights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [bookingStatus, setBookingStatus] = useState(null);

  // Mock data - in a real app, this would come from an API
  const mockFlights = [
    {
      id: 1,
      airline: 'Delta Airlines',
      flightNumber: 'DL123',
      origin: 'JFK',
      destination: 'LAX',
      departureTime: '2025-07-10T08:00:00-04:00',
      arrivalTime: '2025-07-10T11:30:00-07:00',
      price: 299.99,
      seatsAvailable: 24
    },
    {
      id: 2,
      airline: 'United Airlines',
      flightNumber: 'UA456',
      origin: 'JFK',
      destination: 'SFO',
      departureTime: '2025-07-10T09:15:00-04:00',
      arrivalTime: '2025-07-10T13:30:00-07:00',
      price: 349.99,
      seatsAvailable: 12
    },
    {
      id: 3,
      airline: 'American Airlines',
      flightNumber: 'AA789',
      origin: 'JFK',
      destination: 'ORD',
      departureTime: '2025-07-10T07:30:00-04:00',
      arrivalTime: '2025-07-10T09:45:00-05:00',
      price: 199.99,
      seatsAvailable: 8
    },
    {
      id: 4,
      airline: 'Southwest',
      flightNumber: 'WN101',
      origin: 'LAX',
      destination: 'JFK',
      departureTime: '2025-07-11T10:00:00-07:00',
      arrivalTime: '2025-07-11T18:30:00-04:00',
      price: 279.99,
      seatsAvailable: 15
    },
    {
      id: 5,
      airline: 'JetBlue',
      flightNumber: 'B6202',
      origin: 'BOS',
      destination: 'SFO',
      departureTime: '2025-07-12T06:45:00-04:00',
      arrivalTime: '2025-07-12T10:30:00-07:00',
      price: 329.99,
      seatsAvailable: 5
    },
    {
      id: 6,
      airline: 'Alaska Airlines',
      flightNumber: 'AS345',
      origin: 'SEA',
      destination: 'LAX',
      departureTime: '2025-07-13T14:20:00-07:00',
      arrivalTime: '2025-07-13T16:45:00-07:00',
      price: 159.99,
      seatsAvailable: 22
    }
  ];

  // Fetch flights (in a real app, this would be an API call)
  useEffect(() => {
    const fetchFlights = async () => {
      try {
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 800));
        setFlights(mockFlights);
        setFilteredFlights(mockFlights);
        setLoading(false);
      } catch (err) {
        setError('Failed to load flights. Please try again later.');
        setLoading(false);
        console.error('Error fetching flights:', err);
      }
    };

    fetchFlights();
  }, []);

  // Apply filters when they change
  useEffect(() => {
    if (!filters) return;
    
    let result = [...flights];
    
    if (filters.from) {
      result = result.filter(flight => 
        flight.origin.toLowerCase().includes(filters.from.toLowerCase())
      );
    }
    
    if (filters.to) {
      result = result.filter(flight => 
        flight.destination.toLowerCase().includes(filters.to.toLowerCase())
      );
    }
    
    if (filters.maxPrice) {
      result = result.filter(flight => 
        flight.price <= filters.maxPrice
      );
    }
    
    setFilteredFlights(result);
  }, [filters, flights]);

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
      <h2>Available Flights {filters && `(${filteredFlights.length})`}</h2>
      
      {bookingStatus && (
        <div className={`booking-status ${bookingStatus.type}`}>
          {bookingStatus.message}
        </div>
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
                    <span className="label">Date:</span>
                    <span>{formatDate(flight.departureTime)}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Duration:</span>
                    <span>{calculateDuration(flight.departureTime, flight.arrivalTime)}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Seats:</span>
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
                onClick={() => window.location.reload()}
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
