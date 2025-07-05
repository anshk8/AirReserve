class FlightDataService {
  constructor() {
    this.baseUrl = process.env.NODE_ENV === 'production' 
      ? '/api' 
      : '/api'; // Use proxy in development
  }

  async getAllFlights() {
    try {
      const response = await fetch(`${this.baseUrl}/flights`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching flights:', error);
      throw error;
    }
  }

  async getFlightsByRoute(origin, destination) {
    try {
      const response = await fetch(`${this.baseUrl}/flights?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching flights by route:', error);
      throw error;
    }
  }

  async searchFlights(filters = {}) {
    try {
      const queryParams = new URLSearchParams();
      if (filters.from) queryParams.append('origin', filters.from);
      if (filters.to) queryParams.append('destination', filters.to);
      if (filters.maxPrice) queryParams.append('maxPrice', filters.maxPrice);

      const response = await fetch(`${this.baseUrl}/flights?${queryParams.toString()}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error searching flights:', error);
      throw error;
    }
  }
}

export default new FlightDataService(); 