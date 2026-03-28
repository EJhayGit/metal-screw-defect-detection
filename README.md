# Metal Screw Defect Detection

An end-to-end AI application for inspecting metal screws and automating defect detection using Convolutional Neural Networks (CNNs). This system identifies whether a screw is **Normal** (functioning) or **Defective** (scratched, threaded, damaged) using computer vision.

## System Architecture

This project is separated into three core components:

### 1. Backend (`/backend`)
A fast, lightweight REST API built with **FastAPI** to serve the trained machine learning model.
- Receives anomaly images from the mobile app
- Preprocesses images for inference using TensorFlow/Keras
- Returns classification results (Normal/Defective) along with confidence scores
- **Setup**: `pip install -r backend/requirements.txt`, run with `uvicorn main:app --host 0.0.0.0 --port 8000`

### 2. Mobile App (`/mobile`)
A **Flutter** cross-platform application that acts as the user interface for the system.
- Allows users to capture or upload images of screws for inspection
- Integrates seamlessly with the backend Fast API
- Displays diagnostic results in real-time
- **Setup**: Navigate to `/mobile`, install dependencies with `flutter pub get`, open emulator and run `flutter run`.

### 3. Machine Learning Pipeline (`/ml` & `/datasets`)
Python scripts used to streamline model training and dataset preparation. 
- Utilizes TensorFlow/Keras to build and train fine-tuned CNNs based on lightweight architectures like MobileNetV2
- Automates data downloading and segregation for Kaggle datasets
- Exports a trained `model.h5` model to be directly deployed into the backend server

## Getting Started

**Requirements**:
- Python 3.9+
- Flutter SDK
- TensorFlow

**1. Start the API Server**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

**2. Launch the Mobile App**:
```bash
cd mobile
flutter pub get
flutter run
```

*Note: If running on a physical mobile device, ensure it is connected to the same network as the backend server, and update the API base URL in the Flutter application to point to your machine's local IP address instead of `127.0.0.1`.*

## Scope and Limitations
- **Binary Classification**: Designed exclusively for binary defect detection of a specific set of metal screws.
- **Research Only**: This system acts as a proof of concept and is not designed for real-time edge deployment within factory hardware without edge optimizations (e.g., TFLite, TensorRT conversion).
