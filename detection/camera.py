import torch
import cv2
import os
import random
import math

# Function to calculate the change in latitude and longitude based on distance
def distance_to_lat_lon(distance, altitude, latitude, longitude, frame_width):
    """
    Convert distance to changes in latitude and longitude.

    Args:
        distance (float): Distance to the detected human in meters.
        altitude (float): Altitude of the drone in meters.
        latitude (float): Current latitude of the drone in decimal degrees.
        longitude (float): Current longitude of the drone in decimal degrees.
        frame_width (int): Width of the video frame in pixels.

    Returns:
        (float, float): New latitude and longitude after distance change.
    """
    # Approximate conversion factor for degrees to meters on Earth
    meters_per_degree_lat = 111320  # Average meters per degree of latitude
    meters_per_degree_lon = 40008000 / 360  # Meters per degree of longitude at the equator
    
    # Assuming the drone is flying horizontally at a known altitude
    horizontal_fov = 2 * altitude * math.tan(math.radians(45) / 2)  # Horizontal field of view
    pixel_size_meters = horizontal_fov / frame_width  # Convert pixel size to meters

    # Calculate the distance in degrees
    distance_degrees_lat = (distance * pixel_size_meters) / meters_per_degree_lat
    distance_degrees_lon = (distance * pixel_size_meters) / meters_per_degree_lon

    # Calculate new latitude and longitude
    new_latitude = latitude + distance_degrees_lat
    new_longitude = longitude + distance_degrees_lon

    return new_latitude, new_longitude

# Function to calculate distance based on bounding box and altitude
def calculate_distance(bbox, altitude, frame_width, frame_height, fov=45):
    """
    Calculate the distance of the drone from a detected human using the bounding box.

    Args:
        bbox (list): Bounding box coordinates [x_min, y_min, x_max, y_max, confidence, class].
        altitude (float): Altitude of the drone in meters.
        frame_width (int): Width of the video frame in pixels.
        frame_height (int): Height of the video frame in pixels.
        fov (float): Camera field of view in degrees (default: 45).

    Returns:
        float: Calculated distance to the human in meters.
    """
    # Get the center of the bounding box
    x_min, y_min, x_max, y_max = bbox[:4]
    bbox_width = x_max - x_min
    bbox_height = y_max - y_min

    # Calculate the horizontal FOV in meters at the given altitude
    fov_rad = math.radians(fov)
    horizontal_fov_meters = 2 * altitude * math.tan(fov_rad / 2)

    # Calculate the size of one pixel in meters
    pixel_size_meters = horizontal_fov_meters / frame_width

    # Calculate the approximate distance to the human
    bbox_center_x = (x_min + x_max) / 2
    bbox_center_y = (y_min + y_max) / 2
    distance = math.sqrt((bbox_center_x - frame_width / 2) ** 2 + (bbox_center_y - frame_height / 2) ** 2)
    distance_meters = distance * pixel_size_meters

    return distance_meters

# Function to run video detection and calculate distance for a random human
def run_video_detection_with_distance(weights_path, altitude, initial_latitude, initial_longitude, output_dir="output", conf_threshold=0.25):
    """
    Run YOLOv5 detection on a live feed from the drone's USB camera and calculate the distance of a random detected human.

    Args:
        weights_path (str): Path to the YOLOv5 weights file (.pt).
        altitude (float): Altitude of the drone in meters.
        initial_latitude (float): Initial latitude of the drone in decimal degrees.
        initial_longitude (float): Initial longitude of the drone in decimal degrees.
        output_dir (str): Directory to save the detection frame.
        conf_threshold (float): Confidence threshold for detections (default: 0.25).

    Returns:
        None
    """
    # Initialize video capture from USB camera (device index 0, adjust if needed)
    cap = cv2.VideoCapture(0)  # 0 for default camera, change to the appropriate device index if needed
    if not cap.isOpened():
        print("Error: Cannot open video feed from USB camera.")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path)
    model.conf = conf_threshold  # Set confidence threshold

    print("Starting live feed detection...")

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame from camera.")
            break

        frame_count += 1
        frame_height, frame_width = frame.shape[:2]

        # Perform inference on the frame
        results = model(frame)
        detections = results.xyxy[0].cpu().numpy()  # Get detections as numpy array

        if len(detections) > 0:  # If there are any detections
            print(f"Detections found in frame {frame_count}.")

            # Select a random detection
            random_detection = random.choice(detections)
            human_id = int(random_detection[5])  # Human class ID (0 is usually for persons in YOLOv5)

            # Calculate distance to the random detection
            distance = calculate_distance(random_detection, altitude, frame_width, frame_height)
            print(f"Selected Human ID: {human_id}, Calculated distance: {distance:.2f} meters.")

            # Convert distance to latitude and longitude
            new_latitude, new_longitude = distance_to_lat_lon(distance, altitude, initial_latitude, initial_longitude, frame_width)
            print(f"New latitude: {new_latitude:.6f}, New longitude: {new_longitude:.6f}")

            # Annotate and save the frame
            annotated_frame = results.render()[0]  # Render detections on the frame
            output_path = os.path.join(output_dir, f"detection_frame_{frame_count}.jpg")
            cv2.imwrite(output_path, annotated_frame)
            print(f"Frame saved with annotations at {output_path}")

            # Exit after detecting and calculating distance
            break

        # Display the video frame with detections
        annotated_frame = results.render()[0]
        cv2.imshow("Detection Results", annotated_frame)

        # Press 'q' to quit manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Video detection completed.")

# Define paths, altitude, and initial coordinates (latitude, longitude)
weights_path = "yolov5/weights/best.pt"  # Path to your YOLOv5 weights file
altitude = 5.0  # Altitude of the drone in meters
initial_latitude = 12.9716  # Example: Initial latitude of the drone
initial_longitude = 77.5946  # Example: Initial longitude of the drone
output_dir = "output"  # Directory to save the detection frame

# Run the detection with distance calculation
if __name__ == "__main__":
    print("Starting YOLOv5 live feed detection with distance calculation...")
    run_video_detection_with_distance(weights_path, altitude, initial_latitude, initial_longitude, output_dir)
    print("Detection process completed.")

