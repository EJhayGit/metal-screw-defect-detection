from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import io
from PIL import Image
import numpy as np
import os

# Try importing TensorFlow, but don't crash if it's not available
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("Warning: TensorFlow is not installed. Install it with: pip install tensorflow")
    print("The API will run with mock predictions until TensorFlow is available.")

app = FastAPI(title="Metal Screw Defect Detector API")

# Add CORS middleware to allow the Flutter web app to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin (perfect for local dev)
    allow_credentials=False,
    allow_methods=["*"],  # Allows all methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

MODEL_PATH = "model.h5"

# Load model globally
model = None
if TF_AVAILABLE:
    try:
        if os.path.exists(MODEL_PATH):
            model = tf.keras.models.load_model(MODEL_PATH)
            print("Model loaded successfully.")
        else:
            print(f"Warning: Model file not found at {MODEL_PATH}. API will return mock predictions mapped from filename.")
    except Exception as e:
        print(f"Error loading model from {MODEL_PATH}: {e}")
else:
    print("Skipping model loading (TensorFlow not available).")

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((224, 224))  # standard for MobileNetV2
        image_array = np.array(image) / 255.0  # normalize
        image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
        return image_array
    except Exception as e:
        raise ValueError(f"Invalid image file: {e}")

@app.get("/health")
async def health_check():
    return JSONResponse(content={
        "status": "ok",
        "model_loaded": model is not None,
        "tensorflow_available": TF_AVAILABLE
    })

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    print(f"Received file: {file.filename} with content_type: {file.content_type}")
    if file.content_type and not file.content_type.startswith("image/") and file.content_type != "application/octet-stream":
        print(f"Warning: Unexpected content_type {file.content_type}, proceeding anyway.")
    
    contents = await file.read()
    
    try:
        image_tensor = preprocess_image(contents)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    
    if model is None:
        # Mock Response if model not trained yet or TF not available
        is_defective = "defect" in (file.filename or "").lower() or "scratch" in (file.filename or "").lower()
        mock_class = "Defective" if is_defective else "Normal"
        confidence = 0.95 if is_defective else 0.99
        return JSONResponse(content={
            "classification": mock_class,
            "confidence": confidence,
            "raw_score": 0.95 if is_defective else 0.01,
            "info": "Mock prediction (no model loaded)"
        })
    
    # Inference (Diagnostic Version)
    try:
        print("\n--- NEW PREDICTION ---")
        
        # 1. Run the model
        prediction = model.predict(image_tensor)
        print(f"Raw Prediction Array: {prediction}")
        
        # 2. Safely extract the score
        # Using .item() is safer than [0][0] in case the shape is just (1,)
        score = float(prediction.item()) 
        print(f"Extracted Score: {score}")
        
        # 3. Apply the logic
        threshold_for_normal = 0.80 
        
        if score >= threshold_for_normal:
            classification = "Normal"
            confidence = score  
        else:
            classification = "Defective"
            confidence = 1.0 - score  
            
        print(f"Final Decision -> Class: {classification} | Confidence: {confidence}")
        print("----------------------\n")
            
        return JSONResponse(content={
            "classification": classification,
            "confidence": confidence,
            "raw_score": score
        })
    except Exception as e:
        import traceback
        traceback.print_exc() # This will print the exact line that caused the crash in your terminal
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")