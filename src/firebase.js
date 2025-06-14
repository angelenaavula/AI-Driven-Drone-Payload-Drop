// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDPwDzZD0WhYW3e6nquPfwELcllrH72vSg",
  authDomain: "droneproject1-49b2f.firebaseapp.com",
  projectId: "droneproject1-49b2f",
  storageBucket: "droneproject1-49b2f.appspot.com",
  messagingSenderId: "689355327035",
  appId: "1:689355327035:web:353f84d4ce1d1610f2fe1e",
  measurementId: "G-6WKKBVDHYQ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app); // This will be used for authentication
export default app;
