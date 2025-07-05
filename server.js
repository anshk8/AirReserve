import express from 'express';
import path from 'path';
import cors from 'cors';
import { fileURLToPath } from 'url';
import flightDataProcessor from './src/api/flightDataProcessor.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.static(path.join(__dirname, 'src/ui/public')));

// API endpoint to get flight data
app.get('/api/flights', async (req, res) => {
  try {
    const { origin, destination, maxPrice } = req.query;
    
    let flights;
    
    if (origin && destination) {
      flights = await flightDataProcessor.getFlightsByRoute(origin, destination);
    } else {
      flights = await flightDataProcessor.getAllFlights();
    }
    
    // Apply maxPrice filter if provided
    if (maxPrice) {
      flights = flights.filter(flight => flight.price <= parseFloat(maxPrice));
    }
    
    res.json(flights);
  } catch (error) {
    console.error('Error fetching flights:', error);
    res.status(500).json({ error: 'Failed to fetch flight data' });
  }
});

// Serve the main HTML file for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'src/ui/public', 'index.html'));
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
