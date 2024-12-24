#stops after first frame of detection 
import torch
from yolov5 import detect  # Ensure the yolov5 folder is a valid Python module
import cv2
import os

# Function to run detection on a video and stop when any detection occurs
def run_video_detection_stop_on_detection(weights_path, source_path, output_dir="output", img_size=(640, 640), conf_threshold=0.25):
    """
    Run YOLOv5 detection on a video and stop when any detection occurs.

    Args:
        weights_path (str): Path to the YOLOv5 weights file (.pt).
        source_path (str): Path to the video file for detection.
        output_dir (str): Directory to save the detection frame.
        img_size (tuple): Image size for YOLOv5 inference (default: (640, 640)).
        conf_threshold (float): Confidence threshold for detections (default: 0.25).

    Returns:
        None
    """
    # Initialize video capture
    cap = cv2.VideoCapture(source_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video file {source_path}")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path)
    model.conf = conf_threshold  # Set confidence threshold

    print("Starting video detection...")

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading frame.")
            break

        frame_count += 1

        # Perform inference on the frame
        results = model(frame)

        # Check if there are any detections
        detections = results.xyxy[0].cpu().numpy()  # Get detections as numpy array
        if len(detections) > 0:  # If there are any detections
            print("Detection made, saving frame and exiting...")

            # Annotate the frame with detections
            annotated_frame = results.render()[0]  # Render detections on the frame

            # Save the annotated frame
            output_path = os.path.join(output_dir, f"detection_frame_{frame_count}.jpg")
            cv2.imwrite(output_path, annotated_frame)
            print(f"Frame saved with bounding boxes at {output_path}")

            cap.release()
            cv2.destroyAllWindows()
            return  # Exit the function immediately

        # Display the video frame without detections
        annotated_frame = results.render()[0]  # Render detections on the frame
        cv2.imshow("Detection Results", annotated_frame)

        # Press 'q' to quit manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Video detection completed.")

# Define paths
weights_path = "yolov5/weights/best.pt"  # Path to your YOLOv5 weights file
source_path = "/home/kmit/Downloads/video.mp4"  # Path to the input video
output_dir = "output"  # Directory to save the detection frame

# Run the detection
if __name__ == "__main__":
    print("Starting YOLOv5 video detection with early stop on any detection...")
    run_video_detection_stop_on_detection(weights_path, source_path, output_dir)
    print("Detection process completed.")

