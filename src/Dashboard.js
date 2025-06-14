import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import './Dashboard.css';
import { useAuth } from './AuthContext';
import MapComponent from './components/MapComponent';
import axios from 'axios';

function Dashboard() {
  const [missionStatus, setMissionStatus] = useState('');
  const { logout } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      alert('Logout failed: ' + error.message);
    }
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="dashboard-container">
      <aside className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
        <h2>AI Drone Rescue Command Center</h2>
        <ul>
          <li>
            <NavLink to="/missioncontrol" className={({ isActive }) => (isActive ? 'active' : '')}>
              Mission Control
            </NavLink>
          </li>
          <li>
            <NavLink to="/history" className={({ isActive }) => (isActive ? 'active' : '')}>
              History
            </NavLink>
          </li>
          <li>
            <NavLink to="/alerts" className={({ isActive }) => (isActive ? 'active' : '')}>
              Alerts
            </NavLink>
          </li>
          <li>
            <NavLink to="/payloadmanagement" className={({ isActive }) => (isActive ? 'active' : '')}>
              Payload Management
            </NavLink>
          </li>
          <li>
            <NavLink to="/trainingsimulation" className={({ isActive }) => (isActive ? 'active' : '')}>
              Training & Simulation
            </NavLink>
          </li>
          <li>
            <NavLink to="/settings" className={({ isActive }) => (isActive ? 'active' : '')}>
              Settings
            </NavLink>
          </li>
        </ul>
      </aside>

      <main className={`main-content ${isSidebarOpen ? 'expanded' : ''}`}>
        <header className="header">
          <button className="menu-icon" onClick={toggleSidebar}>
            ☰
          </button>
          <span>Welcome, Rescue Operator</span>
          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        </header>

        <section className="dashboard">
          <div className="live-feed">
            <h3>Live Drone Feed</h3>
            <div className="video-feed">
              {/* Placeholder for video feed */}
              <video width="100%" height="auto" controls>
                <source src="your-video-source-url" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
            <div className="feed-info">
              <span>Battery: 75%</span>
              <span>Signal: Strong</span>
              <span>Altitude: 50m</span>
            </div>
          </div>

          <div className="mission-map">
            <h3>Mission Map</h3>
            <MapComponent onDispatchDrone={setMissionStatus} />
            <div className="map-info">
              <span>Area Covered: 78%</span>
              <span>Objects Detected: 12</span>
            </div>
            {missionStatus && <p>{missionStatus}</p>}
          </div>
        </section>
      </main>
    </div>
  );
}

export default Dashboard;
