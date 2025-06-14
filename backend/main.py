from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to the drone
try:
    connection_string = "udp:127.0.0.1:14550"  # Modify with your actual connection string
    vehicle = connect(connection_string, baud=57600, wait_ready=True, heartbeat_timeout=60)
    print("Drone connected successfully.")
except Exception as e:
    print("Failed to connect to the drone:", e)
    vehicle = None

# Data models
class Coordinates(BaseModel):
    latitude: float
    longitude: float
    altitude: float = None  # Optional for general coordinates

class RectangleBounds(BaseModel):
    top_left: Coordinates
    bottom_right: Coordinates

# Function to arm and take off to a specific altitude
def arm_and_takeoff(target_altitude):
    if vehicle is None:
        raise HTTPException(status_code=500, detail="Drone not connected")

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.is_armable:
        print("Waiting for vehicle to initialize...")
        time.sleep(1)

    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)

    while True:
        print(f"Altitude: {vehicle.location.global_relative_frame.alt}")
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# Function to calculate the distance between two points (in meters)
def get_distance_meters(location1, location2):
    dlat = location2.lat - location1.lat
    dlong = location2.lon - location1.lon
    return ((dlat**2) + (dlong**2)) ** 0.5 * 1.113195e5

# Rectangle movement within bounds
def move_within_rectangle(top_left, bottom_right, altitude):
    if vehicle is None:
        raise HTTPException(status_code=500, detail="Drone not connected")

    print("Starting grid traversal")
    step_distance = 0.0002  # Increased step size (approx. 22 meters)
    current_lat = top_left.latitude
    current_lon = top_left.longitude

    # Define direction flag to track movement
    moving_forward = True  # Start by moving left to right
    max_retry = 10  # Maximum retries if drone doesn't reach target
    retry_count = 0

    while current_lat >= bottom_right.latitude:
        if moving_forward:
            # Move from left to right along the current latitude
            while current_lon < bottom_right.longitude:
                target_location = LocationGlobalRelative(current_lat, current_lon, altitude)
                print(f"Moving to: {target_location}")
                vehicle.simple_goto(target_location)

                retry_count = 0
                # Wait until drone reaches target
                while True:
                    distance = get_distance_meters(vehicle.location.global_relative_frame, target_location)
                    if distance < 5:  # Target reached within 5 meters
                        print(f"Reached target at lat: {current_lat}, lon: {current_lon}")
                        break

                    # If it's taking too long to reach the target, retry or move to the next waypoint
                    if retry_count >= max_retry:
                        print(f"Retrying target at lat: {current_lat}, lon: {current_lon}")
                        vehicle.simple_goto(target_location)  # Try moving again
                        retry_count = 0

                    retry_count += 1
                    time.sleep(1)

                # Move horizontally to the right
                current_lon += step_distance

        else:
            # Move from right to left along the current latitude
            while current_lon > top_left.longitude:
                target_location = LocationGlobalRelative(current_lat, current_lon, altitude)
                print(f"Moving to: {target_location}")
                vehicle.simple_goto(target_location)

                retry_count = 0
                # Wait until drone reaches target
                while True:
                    distance = get_distance_meters(vehicle.location.global_relative_frame, target_location)
                    if distance < 5:  # Target reached within 5 meters
                        print(f"Reached target at lat: {current_lat}, lon: {current_lon}")
                        break

                    # If it's taking too long to reach the target, retry or move to the next waypoint
                    if retry_count >= max_retry:
                        print(f"Retrying target at lat: {current_lat}, lon: {current_lon}")
                        vehicle.simple_goto(target_location)  # Try moving again
                        retry_count = 0

                    retry_count += 1
                    time.sleep(1)

                # Move horizontally to the left
                current_lon -= step_distance

        # Once we reach the end of the row, move vertically to the next row
        if current_lat > bottom_right.latitude:
            current_lat -= step_distance  # Move downward in the grid
        else:
            current_lat += step_distance  # Move upward for reverse zigzag

        # Reverse the direction for the next row
        moving_forward = not moving_forward
        print(f"Completed row, now at latitude: {current_lat}, longitude: {current_lon}")

    print("Grid traversal complete")

# Dispatch endpoint for rectangle area
@app.post("/drone/dispatch/rectangle")
async def dispatch_drone_rectangle(bounds: RectangleBounds):
    if vehicle is None:
        raise HTTPException(status_code=500, detail="Drone not connected")

    top_left = bounds.top_left
    bottom_right = bounds.bottom_right

    print(f"Dispatching drone within bounds: Top Left: {top_left}, Bottom Right: {bottom_right}")

    # Arm and take off
    arm_and_takeoff(10)  # Set the altitude as required (e.g., 10 meters)

    # Move within the rectangle
    move_within_rectangle(top_left, bottom_right, 10)

    # Return to home
    print("Returning to home position")
    vehicle.mode = VehicleMode("RTL")

    while not vehicle.location.global_relative_frame.alt <= 1:  # Ensure drone lands safely
        time.sleep(1)

    vehicle.close()
    return {"status": "Drone dispatched and returned home."}
