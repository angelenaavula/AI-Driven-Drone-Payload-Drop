# 🛰️ Autonomous AI-Driven Payload Drone

An intelligent, autonomous drone system designed for **disaster relief and rescue operations**. The drone detects humans from aerial footage, calculates optimal drop points, and autonomously delivers payloads using a YOLOv5-based computer vision model deployed on an edge device (Jetson Nano).

---

## 🚀 Overview

This project brings together real-time AI vision, hardware integration, and autonomous flight control. The system receives mission parameters via a FastAPI backend, processes live drone video on the Jetson Nano using a trained YOLOv5 model, and autonomously navigates to drop payloads near detected humans. Designed for use in post-disaster scenarios, it aims to deliver urgent aid with precision and intelligence.

---

## 📷 Architecture

![System Architecture](./assets/drone_architecture.png)


---

## 🧠 Tech Stack

| Domain              | Technologies Used                                           |
|---------------------|-------------------------------------------------------------|
| AI/ML               | YOLOv5, PyTorch, OpenCV                                     |
| Edge Deployment     | Jetson Nano, Go Pro camera                                     |
| Backend API         | FastAPI                                                     |
| Drone Control       | DroneKit, MAVLink                                           |
| Hardware            | Pixhawk, GPS, Ultrasonic sensors                            |
| Web Interface       | React.js (frontend), FastAPI (backend)                      |
| Communication       | MAVProxy, Telemetry                      |

---

## ⚙️ Features

- **Autonomous Flight**: Drone takes off, travels to target coordinates, and returns.
- **Human Detection**: YOLOv5 model processes aerial video feed in real-time.
- **Payload Drop**: Calculates optimal drop point based on bounding box & GPS.
- **Web Interface**: FastAPI backend accepts mission inputs from the admin.
- **Obstacle Avoidance**: Uses sensors to detect and avoid physical obstacles.
- **Live Tracking**: Displays drone’s position, flight status, and detection results.

---


