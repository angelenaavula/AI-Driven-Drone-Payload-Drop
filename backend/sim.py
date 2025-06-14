# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

app = FastAPI()

# Connect to the vehicle
connection_string = "COM5"  # Replace with your connection details
vehicle = connect(connection_string, baud=57600, wait_ready=False, heartbeat_timeout=60)

# Request model for coordinates
class Coordinates(BaseModel):
    latitude: float
    longitude: float
    altitude: float

# Arm and takeoff function
def arm_and_takeoff(target_altitude):
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialize...")
        time.sleep(1)
    
    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)

    while True:
        print(f" Altitude: {vehicle.location.global_relative_frame.alt}")
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

@app.post("/drone/takeoff")
async def takeoff(coords: Coordinates):
    arm_and_takeoff(coords.altitude)
    return {"status": "Taking off", "altitude": coords.altitude}

@app.post("/drone/dispatch")
async def dispatch_drone(coords: Coordinates):
    target_location = LocationGlobalRelative(coords.latitude, coords.longitude, coords.altitude)
    vehicle.simple_goto(target_location)
    return {"status": "Drone dispatched", "target": target_location}

@app.post("/drone/rtl")
async def return_to_launch():
    vehicle.mode = VehicleMode("RTL")
    return {"status": "Returning to Launch"}

@app.on_event("shutdown")
def shutdown_event():
    print("Closing vehicle connection")
    vehicle.close()
