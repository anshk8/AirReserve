import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class FlightDataProcessor {
  constructor() {
    this.dataDir = path.join(__dirname, '../../data');
  }

  async getAllFlightFiles() {
    try {
      const files = await fs.readdir(this.dataDir);
      return files.filter(file => file.startsWith('flight_prices_') && file.endsWith('.json'));
    } catch (error) {
      console.error('Error reading data directory:', error);
      return [];
    }
  }

  async readFlightFile(filename) {
    try {
      const filePath = path.join(this.dataDir, filename);
      const data = await fs.readFile(filePath, 'utf8');
      return JSON.parse(data);
    } catch (error) {
      console.error(`Error reading flight file ${filename}:`, error);
      return null;
    }
  }

  transformFlightData(rawData, route) {
    if (!rawData || !rawData.searches || rawData.searches.length === 0) {
      return [];
    }

    const flights = [];
    let flightId = 1;

    // Get the most recent search
    const latestSearch = rawData.searches[rawData.searches.length - 1];
    
    if (latestSearch.flights && latestSearch.flights.length > 0) {
      latestSearch.flights.forEach((flight, index) => {
        // Parse route to extract origin and destination
        const routeParts = route.split(' to ');
        const origin = routeParts[0] || 'Unknown';
        const destination = routeParts[1] || 'Unknown';

        // Generate realistic flight times based on route
        const departureTime = this.generateDepartureTime();
        const arrivalTime = this.generateArrivalTime(departureTime, origin, destination);

        // Generate realistic flight number
        const flightNumber = this.generateFlightNumber(flight.airline);

        // Generate realistic seats available
        const seatsAvailable = Math.floor(Math.random() * 30) + 1;

        flights.push({
          id: flightId++,
          airline: flight.airline === 'Multiple Airlines' ? this.getRandomAirline() : flight.airline,
          flightNumber: flightNumber,
          origin: origin,
          destination: destination,
          departureTime: departureTime,
          arrivalTime: arrivalTime,
          price: flight.price,
          seatsAvailable: seatsAvailable,
          source: flight.source,
          timestamp: flight.timestamp
        });
      });
    }

    return flights;
  }

  generateDepartureTime() {
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    // Random hour between 6 AM and 10 PM
    const hour = Math.floor(Math.random() * 16) + 6;
    const minute = Math.floor(Math.random() * 60);
    
    tomorrow.setHours(hour, minute, 0, 0);
    return tomorrow.toISOString();
  }

  generateArrivalTime(departureTime, origin, destination) {
    const departure = new Date(departureTime);
    
    // Estimate flight duration based on route (simplified)
    let durationHours = 2; // Default 2 hours
    
    if (origin === 'Vancouver' && destination === 'Toronto') {
      durationHours = 4.5;
    } else if (origin === 'Toronto' && destination === 'Ottawa') {
      durationHours = 1.5;
    } else if (origin === 'Calgary' && destination === 'Edmonton') {
      durationHours = 1;
    } else if (origin === 'Ottawa' && destination === 'Montreal') {
      durationHours = 1;
    }
    
    const arrival = new Date(departure.getTime() + (durationHours * 60 * 60 * 1000));
    return arrival.toISOString();
  }

  generateFlightNumber(airline) {
    const airlines = {
      'Multiple Airlines': ['AC', 'WS', 'PD', 'F8'],
      'Air Canada': ['AC'],
      'WestJet': ['WS'],
      'Porter Airlines': ['PD'],
      'Flair Airlines': ['F8']
    };
    
    const codes = airlines[airline] || ['AC'];
    const code = codes[Math.floor(Math.random() * codes.length)];
    const number = Math.floor(Math.random() * 9999) + 1000;
    
    return `${code}${number}`;
  }

  getRandomAirline() {
    const airlines = ['Air Canada', 'WestJet', 'Porter Airlines', 'Flair Airlines'];
    return airlines[Math.floor(Math.random() * airlines.length)];
  }

  async getAllFlights() {
    try {
      const flightFiles = await this.getAllFlightFiles();
      let allFlights = [];

      for (const file of flightFiles) {
        const rawData = await this.readFlightFile(file);
        if (rawData) {
          const route = rawData.route;
          const flights = this.transformFlightData(rawData, route);
          allFlights = allFlights.concat(flights);
        }
      }

      return allFlights;
    } catch (error) {
      console.error('Error getting all flights:', error);
      return [];
    }
  }

  async getFlightsByRoute(origin, destination) {
    try {
      const allFlights = await this.getAllFlights();
      
      return allFlights.filter(flight => 
        flight.origin.toLowerCase().includes(origin.toLowerCase()) &&
        flight.destination.toLowerCase().includes(destination.toLowerCase())
      );
    } catch (error) {
      console.error('Error getting flights by route:', error);
      return [];
    }
  }

  async searchFlights(filters = {}) {
    try {
      let flights = await this.getAllFlights();

      if (filters.origin) {
        flights = flights.filter(flight => 
          flight.origin.toLowerCase().includes(filters.origin.toLowerCase())
        );
      }

      if (filters.destination) {
        flights = flights.filter(flight => 
          flight.destination.toLowerCase().includes(filters.destination.toLowerCase())
        );
      }

      if (filters.maxPrice) {
        flights = flights.filter(flight => 
          flight.price <= parseFloat(filters.maxPrice)
        );
      }

      return flights;
    } catch (error) {
      console.error('Error searching flights:', error);
      return [];
    }
  }
}

export default new FlightDataProcessor(); 