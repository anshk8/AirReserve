import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

// Import global styles
import './index.css';

// Get the root element
const container = document.getElementById('root');
const root = createRoot(container);

// Render the App component
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
