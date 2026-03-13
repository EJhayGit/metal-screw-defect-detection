# metal-screw-defect-detection
# Automated Defect Detection in Metal Screws Using Convolutional Neural Networks

## Overview
This project focuses on the automated detection of defects in metal screws using Convolutional Neural Networks (CNNs). The goal is to improve industrial quality inspection by identifying defective screws from image data and classifying them as either **normal** or **defective**.

The study explores a computer vision pipeline using a CNN-based classifier or a lightweight segmentation model, with an additional anomaly detection baseline for comparison. The system is intended for research and experimental evaluation under controlled conditions.

## Objectives
- Develop a CNN-based model for detecting defects in metal screws
- Classify screw images as **normal** or **defective**
- Optionally localize defects using a lightweight segmentation model
- Compare the CNN model against an anomaly detection baseline
- Evaluate performance using standard computer vision metrics

## Scope
This project is limited to:
- Image-based defect detection of **metal screws**
- Binary classification: **normal** vs. **defective**
- Optional defect localization using segmentation
- Offline experimentation only

This project does **not** include:
- Real-time factory deployment
- Mechanical strength testing
- Detection of other fasteners or hardware components
- Non-visual inspection methods

## Dataset
The project uses an openly available dataset containing images of metal screws with normal and defective samples.

Possible sources include:
- MVTec AD dataset
- Kaggle screw defect datasets
- Other open academic or research datasets with proper licensing
