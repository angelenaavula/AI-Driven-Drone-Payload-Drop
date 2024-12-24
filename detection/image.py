#Takes input image, performs detections, saves output in a location
import torch
from yolov5 import detect  # Ensure the yolov5 folder is a valid Python module

# Function to run detection on an image
def run_detection(weights_path, source_path, img_size=(640, 640), conf_threshold=0.25):
    """
    Run YOLOv5 detection on an image.

    Args:
        weights_path (str): Path to the YOLOv5 weights file (.pt).
        source_path (str): Path to the image file for detection.
        img_size (tuple): Image size for YOLOv5 inference (default: (640, 640)).
        conf_threshold (float): Confidence threshold for detections (default: 0.25).

    Returns:
        None
    """
    try:
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
            exist_ok=False,
            line_thickness=3,
            hide_labels=False,
            hide_conf=False,
        )
    except Exception as e:
        print(f"An error occurred: {e}")

# Define paths
weights_path = "yolov5/weights/best.pt"  # Path to your YOLOv5 weights file
source_path = "/home/kmit/Downloads/aerial2.jpeg"  # Path to the input image

# Run the detection
if __name__ == "__main__":
    print("Starting YOLOv5 detection...")
    run_detection(weights_path, source_path)
    print("Detection completed. Check the 'runs/detect/exp' directory for results.")

