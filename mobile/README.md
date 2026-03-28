# Screw Defect Detector Mobile App

A Flutter application serving as the frontend client for the Metal Screw Defect Detection system. 

## Features
- **Image Upload**: Select images from the device gallery.
- **Real-time Diagnostics**: Connects to the FastAPI backend to provide predictions on whether a given screw image reveals a Defective or Normal screw.
- **Confidence Indicators**: Extracts and displays confidence scores directly on the UI for analytical metrics.

## Running the App

1. Ensure the backend FastAPI server is actively running. 
   - *Note: If you are running the app on a physical device, make sure your device and the backend server are on the same local network. Update the API URL in the Flutter code (`lib/...`) to match your host machine's IP address. For Android emulators pointing to the host machine, you typically use `http://10.0.2.2:8000`.*
2. Inside the `/mobile` directory, fetch the required dependencies:
   ```bash
   flutter pub get
   ```
3. Run the application:
   ```bash
   flutter run
   ```
