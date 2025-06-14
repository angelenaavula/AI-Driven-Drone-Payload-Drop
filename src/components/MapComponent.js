import React, { useState, useCallback } from 'react';
import { GoogleMap, useLoadScript } from '@react-google-maps/api';
import axios from 'axios';

const libraries = ['drawing'];

const MapComponent = ({ onDispatchDrone }) => {
  const [selectedArea, setSelectedArea] = useState(null);
  const [drawingManager, setDrawingManager] = useState(null);

  const center = {
    lat: 17.39716,
    lng: 78.49040,
  };

  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: 'AIzaSyB-6NuWru71NBpaRmAaiEZjRmTJnUfQBbQ',  // Replace with your API Key
    libraries,
  });

  const mapContainerStyle = {
    height: '500px',
    width: '100%',
  };

  const mapOptions = {
    zoom: 18,
    center: center,
    mapTypeId: 'satellite',
    mapTypeControl: false,
    streetViewControl: false,
    fullscreenControl: true,
    zoomControl: true,
  };

  const onLoad = useCallback((map) => {
    console.log("Map loaded");

    const drawingManagerInstance = new window.google.maps.drawing.DrawingManager({
      drawingMode: null,
      drawingControl: true,
      drawingControlOptions: {
        position: window.google.maps.ControlPosition.TOP_CENTER,
        drawingModes: [
          window.google.maps.drawing.OverlayType.RECTANGLE,
        ],
      },
    });

    drawingManagerInstance.setMap(map);
    setDrawingManager(drawingManagerInstance);

    // Listener for when rectangle is drawn
    window.google.maps.event.addListener(drawingManagerInstance, 'rectanglecomplete', (rectangle) => {
      console.log("Rectangle complete:", rectangle);

      const bounds = rectangle.getBounds();
      const selectedBounds = bounds.toJSON();
      console.log("Selected Bounds:", selectedBounds);

      setSelectedArea(selectedBounds); // Set selected area for drone dispatch
    });
  }, []);

  const handleDispatchDrone = async () => {
    if (selectedArea) {
      try {
        console.log("Dispatching drone with selected area:", selectedArea);
  
        // Round the coordinates to 6 decimal places
        const requestData = {
          top_left: {
            latitude: parseFloat(selectedArea.north).toFixed(6),
            longitude: parseFloat(selectedArea.west).toFixed(6),
          },
          bottom_right: {
            latitude: parseFloat(selectedArea.south).toFixed(6),
            longitude: parseFloat(selectedArea.east).toFixed(6),
          },
        };
        
        console.log("Sending request to backend:", requestData);
  
        const response = await axios.post('http://172.168.0.157:3001/drone/dispatch/rectangle', requestData);
        console.log('Drone dispatched:', response.data); // Log the response from the backend
      } catch (error) {
        console.error('Error dispatching drone:', error);
        alert('Failed to dispatch drone');
      }
    } else {
      alert('No area selected');
    }
  };
  

  const onUnmount = useCallback(() => {
    if (drawingManager) {
      drawingManager.setMap(null);
    }
  }, [drawingManager]);

  if (loadError) {
    return <div className="p-4 text-red-500">Error loading maps</div>;
  }

  if (!isLoaded) {
    return <div className="p-4">Loading maps...</div>;
  }

  return (
    <div className="w-full">
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        options={mapOptions}
        onLoad={onLoad}
        onUnmount={onUnmount}
      />
      {selectedArea && (
        <button onClick={handleDispatchDrone} className="dispatch-button">
          Dispatch Drone
        </button>
      )}
    </div>
  );
};

export default MapComponent;
