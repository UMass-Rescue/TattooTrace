# TattooTrace

## Introduction

TattooTrace integrates advanced machine learning models like YOLOv5 and CLIP to analyze and identify tattoos from images and videos. Leveraging the robust backend of [Immich](https://github.com/immich-app/immich), this tool aims to support efforts to combat and understand human trafficking dynamics.

## Installation Instructions

### Requirements
- Docker Desktop
- npm
- Makefile (for UNIX-like operating systems)

### Setting Up the YOLOv5 (Localization)

1. **Clone the YOLOv5 Repository**
    ```bash
    git clone https://github.com/ultralytics/yolov5
    cd yolov5
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Download Pre-trained Weights**
Download the YOLOv5s model weights [Link](https://drive.google.com/file/d/14VpsSrTkOxp0MTzN7uaVJp8uAZ167l-z/view?usp=sharing)

4. **Inference**
    - To perform inference on images:
    ```bash
    cd 
    python detect.py --source /path/to/images --weights best.pt --conf 0.25
    ```
    - To perform inference on video:
    ```bash
    python detect.py --source /path/to/video.mp4 --weights best.pt --conf 0.25
    ```
5. **Output**
   ```
   cd yolov5 Tattoo Recognition/detected/exp6
   ```

### Setting Up the CLIP (Recognition & Analysis)

1. **Frontend Setup**
    ```bash
    cd clip/frontend/clip-app
    npm install
    npm start
    ```
   This will start the frontend application at `http://localhost:3000`.

2. **Backend Setup**
    ```bash
    cd clip/backend/
    python app.py
    ```

### Setting Up the Immich-Based Application

1. **Environment Setup**
    Ensure Docker Desktop is installed and running on your system. Navigate to the main Immich directory:
    ```bash
    cd immich
    ```

2. **Configuration**
    Modify `docker/.env` to set the `UPLOAD_LOCATION` environment variable.

3. **Model Weights**
    Download the model weights and place them in:
    ```
    /immich/machine-learning/app/models/weight/
    ```
    - Download link for weight file: [https://drive.google.com/file/d/14VpsSrTkOxp0MTzN7uaVJp8uAZ167l-z/view?usp=sharing]

4. **Build and Run**
    From the Immich directory, execute:
    ```bash
    make dev
    ```
   Access the development instance at `http://localhost:3000`.

## Features

### Current Functionality (YOLOv5 & CLIP)
- **Tattoo Detection**: Utilizes YOLOv5 to detect tattoos with a configurable minimum confidence score.
- **Tattoo Recognition**: Using the Clip model to recognize and analyze a given tattoo with its meaning.
- **Tattoo Clustering**: To cluster similar tattoos based on the CLIP output from the given prompt.
- **User Interaction**: Simple user interface to trigger tattoo detection.

### Current Functionality for Immich-Based Application
- The user can press the button to trigger the tattoo detection function.
- Use YOLOv5 to detect tattoos in the photos.
- Adjust the setting for the minimum confidence score for the model.

## Data Collection
- **[NTU Dataset](https://github.com/xiamenwcy/NTU_Dataset/blob/master/README.md)**: Contains 32,145 images of tattoos without labels.
- **Labeled Tattoo Images**: Collected 1,000 images with bounding box labels.

## Model Information

### YOLOv5
- Utilized for tattoo detection with bounding box regression.
- Model trained on labelled tattoo dataset.
- [YOLOv5 GitHub Repository](https://github.com/ultralytics/yolov5)

### CLIP (Contrastive Language-Image Pre-Training)
- Used for recognizing and interpreting the context and significance of tattoos.
- Demonstrates impressive zero-shot performance.
- [CLIP Model Information](https://openai.com/research/clip)

### Future Enhancements
- **Expand Object Detection**: Plan to upgrade from YOLOv5 to State-of-the-art model for enhanced accuracy and speed.
- **CLIP Integration**: Improve tattoo recognition and contextual understanding by integrating CLIP into the Immich framework.
- **Enhanced Clustering Algorithms**: Develop sophisticated algorithms to categorize and analyze tattoos more effectively.
- **Video Timestamps Display**: Implement functionality to display video timestamps post-clustering analysis.

## Contributing
Contributions are welcome! Please refer to the CONTRIBUTING.md for guidelines on how to contribute effectively to this project.
