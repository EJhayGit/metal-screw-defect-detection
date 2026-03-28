import os
import shutil
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
INCOMING_DIR = os.path.join(BASE_DIR, 'datasets', 'incoming')
NORMAL_DIR = os.path.join(BASE_DIR, 'datasets', 'merged', 'Normal')
DEFECTIVE_DIR = os.path.join(BASE_DIR, 'datasets', 'merged', 'Defective')
MODEL_PATH = os.path.join(BASE_DIR, 'backend', 'model.h5')

# Ensure directories exist
os.makedirs(NORMAL_DIR, exist_ok=True)
os.makedirs(DEFECTIVE_DIR, exist_ok=True)

def preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}. Cannot auto-segregate.")
        return

    print(f"Loading model from {MODEL_PATH}...")
    model = tf.keras.models.load_model(MODEL_PATH)
    
    files = [f for f in os.listdir(INCOMING_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"Found {len(files)} images to segregate.")

    segregated_count = {"Normal": 0, "Defective": 0}

    for filename in files:
        file_path = os.path.join(INCOMING_DIR, filename)
        try:
            image_tensor = preprocess_image(file_path)
            prediction = model.predict(image_tensor)
            score = float(prediction[0][0])
            
            # Use 0.5 threshold (Same as backend/main.py logic)
            # Backend logic: score > 0.5 -> Normal, else Defective
            if score > 0.5:
                target_dir = NORMAL_DIR
                label = "Normal"
            else:
                target_dir = DEFECTIVE_DIR
                label = "Defective"
                
            shutil.move(file_path, os.path.join(target_dir, filename))
            segregated_count[label] += 1
            print(f"Moved {filename} to {label} (Score: {score:.4f})")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("\n--- Segregation Summary ---")
    print(f"Total processed: {len(files)}")
    print(f"Normal: {segregated_count['Normal']}")
    print(f"Defective: {segregated_count['Defective']}")
    print("---------------------------\n")

if __name__ == "__main__":
    main()
