# VisionFit: Computer Vision-Based Exercise Motion Analysis

A Python and Streamlit-based computer vision prototype for image processing, video motion visualization, and exercise-video movement analysis using OpenCV.

## Overview

VisionFit is a computer vision application that allows users to upload images and exercise videos for visual analysis. It applies image-processing techniques and frame-difference analysis to demonstrate how computer vision can be used to identify and visualize movement.

## Features

### Image Analysis

* **Grayscale conversion:** Converts color images into grayscale.
* **Edge detection:** Uses the Canny edge detector to identify image boundaries.
* **Histogram equalization:** Enhances image contrast.
* **Gaussian blur:** Reduces image noise and smooths details.
* **Original vs. processed comparison:** Displays the uploaded image alongside its processed version.

### Video Motion Analysis

* **Frame differencing:** Compares consecutive video frames to identify changes.
* **Motion visualization:** Highlights regions that have changed between frames.
* **Thresholding:** Separates significant changes from minor pixel variations.
* **Contour visualization:** Displays detected regions of movement.
* **Basic movement estimation:** Provides a rough estimate of movement cycles.

### Streamlit Interface

* Simple and interactive web interface.
* Image and video upload options.
* Selectable image-processing methods.
* Visual results displayed directly in the application.

## Technologies Used

* **Python 3.13**
* **Streamlit** — Interactive web application
* **OpenCV** — Image processing and video analysis
* **NumPy** — Numerical operations
* **ImageIO-FFmpeg** — Video encoding support

## Project Structure

```text
VisionFit/
│
├── app.py
├── requirements.txt
├── README.md
├── statement.md
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── image_tools.py
│   ├── video_tools.py
│   └── pose_tools.py
│
├── docs/
│   ├── design.md
│   └── requirements.md
│
└── tests/
    └── test_core.py
```

## Installation and Setup

### Prerequisites

* Python 3.13
* Git
* Visual Studio Code (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/vedanganand/VisionFit-Computer-Vision-Based-Exercise-Motion-Analysis.git
cd VisionFit-Computer-Vision-Based-Exercise-Motion-Analysis
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
py -3.13 -m venv .venv
```

### 3. Activate the Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If the virtual environment already exists, activate it instead of creating it again.

### 4. Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install --only-binary=:all: -r requirements.txt
```

### 5. Run the Application

```powershell
python -m streamlit run app.py
```

The application will open in your browser. If it does not open automatically, use the local URL displayed in the terminal.

## How to Use

1. Launch the application.
2. Choose **Image Analysis** or **Video Analysis** from the sidebar.
3. Upload an image or a short video.
4. Select the desired processing method, where applicable.
5. View the processed output and motion-analysis results.

## Computer Vision Concepts

This project demonstrates several fundamental computer vision techniques:

* Image enhancement
* Grayscale image conversion
* Canny edge detection
* Gaussian smoothing
* Histogram equalization
* Frame differencing
* Binary thresholding
* Contour detection and visualization

## Limitations

* The exercise analyzer uses frame-difference motion analysis rather than body-pose estimation.
* It does not detect anatomical landmarks or calculate joint angles.
* Repetition estimates are approximate and are not validated exercise-specific counts.
* Motion detection can be affected by lighting changes, camera movement, background activity, and video quality.
* The application is a computer vision prototype and does not provide medical advice or validated exercise coaching.

## Future Improvements

* Integrate pose estimation for body-landmark detection.
* Calculate joint angles for selected exercises.
* Improve repetition counting using joint-angle changes.
* Add exercise-specific movement analysis.
* Improve the accuracy and reliability of video processing.
* Add performance metrics and analysis visualizations.

## Disclaimer

VisionFit is an educational computer vision prototype intended for experimentation and demonstration. Its movement estimates are approximate and should not be used for medical diagnosis, rehabilitation decisions, or professional exercise assessment.

