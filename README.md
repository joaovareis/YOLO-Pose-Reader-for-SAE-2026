# YOLO26 Analog Manometer Reader

![YOLOv8](https://img.shields.io/badge/YOLO26-Pose-red)
![Python](https://img.shields.io/badge/python-3.8+-blue?logo=python)
![OpenCV](https://img.shields.io/badge/opencv-4.x-green?logo=opencv)
![License](https://img.shields.io/badge/license-MIT-green)

A real-time computer vision system that reads **analog manometers** using **pose estimation**. The model detects keypoints on the gauge and converts the needle position into a numerical value.
This project is not an original idea. It is a new 'ROSless' implementation of past works from SEMEAR NRA Group for the current SAE edition, made for testing.

---

## Overview

This project estimates the reading of an analog manometer by:

1. **Detecting keypoints** using a custom YOLO26 pose model
2. **Computing the needle angle** relative to a reference
3. **Mapping the angle** to a calibrated measurement scale
4. **Stabilizing the output** using a median filter

The result is displayed in real time directly on the video stream.

---

## Tech Stack

* **Language**: Python 3
* **Vision**: OpenCV
* **Model**: YOLO26 Pose (`ultralytics`)
* **Math**: NumPy + custom geometric utilities
* **Config**: YAML (camera calibration)

---

## System Architecture

The project is modular and divided into three main components:

### 1. Main Application (`yolo_reading.py`)

* Initializes camera stream
* Applies lens undistortion using calibration data
* Runs the processing loop
* Applies a median filter (5 frames) for stability
* Displays final reading on screen

#DISCLAIMER: The camera YAML file needs to be generated for your specific camera. The file in this repository was generated using ROS1 utilities.

---

### 2. Vision Module (`yolo_stream.py`)

* Loads the trained model (`synth.pt`)
* Performs inference on each frame
* Extracts keypoints from detections

#DISCLAIMER: The synth.pt file is not included because it could potentially be used by competitors during SAE.

**Keypoints detected:**

| Index | Description      |
| ----- | ---------------- |
| 0     | Needle Tip       |
| 1     | Manometer Center |
| 2     | Manometer Base   |

---

### 3. Math & Conversion (`utillitary.py`)

* Builds geometric vectors
* Computes angular displacement
* Maps angle → measurement scale
