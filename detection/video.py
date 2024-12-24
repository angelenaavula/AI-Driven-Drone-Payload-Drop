import torch
from yolov5 import detect  # Ensure the yolov5 folder is a valid Python module
import cv2
import os

# Function to run detection on a video and display output
def run_video_detection(weights_path, source_path, img_size=(640, 640), conf_threshold=0.25):
    """
    Run YOLOv5 detection on a video and display the output.

    Args:
        weights_path (str): Path to the YOLOv5 weights file (.pt).
        source_path (str): Path to the video file for detection.
        img_size (tuple): Image size for YOLOv5 inference (default: (640, 640)).
        conf_threshold (float): Confidence threshold for detections (default: 0.25).

    Returns:
        None
    """
    try:
        # Run YOLOv5 detection
        detect.run(
            weights=weights_path,
            source=source_path,
            imgsz=img_size,  # Tuple for width and height
            conf_thres=conf_threshold,
            iou_thres=0.45,
            max_det=1000,
            device='cpu',  # Change to '0' for GPU
            view_img=False,
            save_txt=False,
            save_conf=False,
            save_crop=False,
            nosave=False,
            classes=None,
            agnostic_nms=False,
            augment=False,
            project="runs/detect",
            name="exp",
            exist_ok=True,  # Prevent creating duplicate folders
            line_thickness=3,
            hide_labels=False,
            hide_conf=False,
        )

        # Get the processed video path
        output_dir = os.path.join("runs/detect", "exp")  # Default YOLOv5 output folder
        output_video_path = os.path.join(output_dir, os.path.basename(source_path))

        if os.path.exists(output_video_path):
            print(f"Displaying result video: {output_video_path}")

            # Read and display the output video
            cap = cv2.VideoCapture(output_video_path)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow("Detection Results", frame)

                # Press 'q' to quit the video display
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
        else:
            print(f"Output video not found at {output_video_path}. Check YOLOv5 settings.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Define paths
weights_path = "yolov5/weights/best.pt"  # Path to your YOLOv5 weights file
source_path = "/home/kmit/Downloads/video.mp4"  # Path to the input video

# Run the detection
if __name__ == "__main__":
    print("Starting YOLOv5 video detection...")
    run_video_detection(weights_path, source_path)
    print("Video detection completed.")

