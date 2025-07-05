const express = require('express');
const path = require('path');
const cors = require('cors');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));

// API endpoint to get flight data
app.get('/api/flights', (req, res) => {
  // In a real app, this would fetch from a database or external API
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
    }
  ];
  
  res.json(mockFlights);
});

// Serve the main HTML file for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log(`Flight data available at http://localhost:${PORT}/api/flights`);
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
  console.error('Unhandled Rejection:', err);
});
