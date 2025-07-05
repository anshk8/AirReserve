// Import the necessary Firebase modules
import { initializeApp } from "firebase/app";

// Your Firebase config here
const firebaseConfig = {
    projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID || process.env.FIREBASE_PROJECT_ID,
    authDomain: `${process.env.REACT_APP_FIREBASE_PROJECT_ID || process.env.FIREBASE_PROJECT_ID}.firebaseapp.com`,
    databaseURL: process.env.REACT_APP_FIREBASE_DATABASE_URL || process.env.FIREBASE_DATABASE_URL,
    storageBucket: `${process.env.REACT_APP_FIREBASE_PROJECT_ID || process.env.FIREBASE_PROJECT_ID}.appspot.com`,
};

// Validate configuration
if (!firebaseConfig.projectId || !firebaseConfig.databaseURL) {
    console.error('Firebase configuration is incomplete:', firebaseConfig);
    throw new Error('Firebase configuration is missing required environment variables. Please check your .env file.');
}

// Initialize Firebase
let configDatabase;
try {
    configDatabase = initializeApp(firebaseConfig);
    console.log('Firebase initialized successfully with project:', firebaseConfig.projectId);
} catch (error) {
    console.error('Error initializing Firebase:', error);
    throw error;
}

export default configDatabase;
