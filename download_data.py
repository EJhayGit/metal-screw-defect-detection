import os
import subprocess

def download_data():
    """Downloads the MVTec AD screw dataset from Kaggle."""
    dataset = "ruruamour/screw-dataset"
    print(f"Downloading {dataset}...")
    try:
        subprocess.run(["kaggle", "datasets", "download", "-d", dataset, "--unzip"], check=True)
        print("Download complete.")
    except Exception as e:
        print(f"Error: {e}. Ensure kaggle.json is configured.")

if __name__ == "__main__":
    download_data()
