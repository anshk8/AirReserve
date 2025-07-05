import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.js';

// Import global styles
import './index.css';

// Get the root elementx
const container = document.getElementById('root');

if (!container) {
  console.error('Root element not found!');
  document.body.innerHTML = '<h1>Error: Root element not found</h1>';
} else {
  try {
    const root = createRoot(container);
    
    // Render the App component
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
    
    console.log('React app mounted successfully!');
  } catch (error) {
    console.error('Error mounting React app:', error);
    container.innerHTML = `<h1>Error loading app: ${error.message}</h1>`;
  }
}
