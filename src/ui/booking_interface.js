import { Windsurf } from 'windsurf';

const BookingInterface = () => {
  const flights = require('../data/flight_prices.json');
  return (
    <div>
      {flights.map(flight => (
        <div key={flight.id}>
          <p>{flight.airline} to {flight.destination}: ${flight.price}</p>
          <button onClick={() => handleBook(flight)}>Book</button>
        </div>
      ))}
    </div>
  );
};

export default BookingInterface;