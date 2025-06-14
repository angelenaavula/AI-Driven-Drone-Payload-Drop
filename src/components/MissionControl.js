import React from 'react';
import './MissionControl.css';

function MissionControl() {
  return (
    <section className="dashboard">
      <div className="live-feed">
        <h3>Live Drone Feed</h3>
        <div className="video-feed">Live Video Feed</div>
        <div className="feed-info">
          <span>Battery: 75%</span>
          <span>Signal: Strong</span>
          <span>Altitude: 50m</span>
        </div>
      </div>
      <div className="mission-map">
        <h3>Mission Map</h3>
        <div className="interactive-map">Interactive Mission Map</div>
        <div className="map-info">
          <span>Active Drones: 3</span>
          <span>Area Covered: 78%</span>
          <span>Objects Detected: 12</span>
        </div>
      </div>
    </section>
  );
}

export default MissionControl;
