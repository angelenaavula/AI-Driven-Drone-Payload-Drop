import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './Dashboard';
import MissionControl from './components/MissionControl';
import ObjectRecognition from './components/ObjectRecognition';
import Alerts from './components/Alerts';
import PayloadManagement from './components/PayloadManagement';
import TrainingSimulation from './components/TrainingSimulation';
import Settings from './components/Settings';
import Login from './components/Login'; // Import the Login component
import { AuthProvider, useAuth } from './AuthContext'; // Assuming AuthContext is set up
import Register from "./components/Register";

// Protected Route Component
const ProtectedRoute = ({ element }) => {
  const { currentUser } = useAuth();
  return currentUser ? element : <Login />;
};

function App() {
  return (
    <AuthProvider>  {/* Wrap the app with AuthProvider */}
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path = "/register" element={<Register/>} /> {/* Public login route */}
          
          {/* Protected routes */}
          <Route path="/" element={<ProtectedRoute element={<Dashboard />} />} />
          <Route path="/objectrecognition" element={<ProtectedRoute element={<ObjectRecognition />} />} />
          <Route path="/alerts" element={<ProtectedRoute element={<Alerts />} />} />
          <Route path="/payloadmanagement" element={<ProtectedRoute element={<PayloadManagement />} />} />
          <Route path="/trainingsimulation" element={<ProtectedRoute element={<TrainingSimulation />} />} />
          <Route path="/settings" element={<ProtectedRoute element={<Settings />} />} />
          <Route path="/missioncontrol" element={<ProtectedRoute element={<MissionControl />} />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
