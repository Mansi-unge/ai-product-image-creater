# AI Product Image Extractor (Frontend)

A modern React frontend for extracting product images from YouTube videos.  
Users can enter a YouTube video URL, preview the thumbnail, and simulate processing with beautiful UI effects.

---

##  Features
- Modern responsive design (Tailwind CSS)
- Smooth animations (Framer Motion)
- YouTube thumbnail preview
- Simulated video processing
- Glassmorphism + gradient UI

---

##  Tech Stack
- React (Vite)
- Tailwind CSS
- Framer Motion
- React Icons

---

##  Setup

```bash
# Install dependencies
npm install

# Run the development server
npm run dev
App runs at  http://localhost:5173
```

# Product Segmentation Workflow using Rembg

## Overview
This project extracts key frames from videos and performs background removal (segmentation) on each frame using the open-source **Rembg** library powered by the **U²-Net** model.  
The output includes segmented product images with transparent backgrounds, ready for enhancement or further AI processing.

---

## Tech Stack
- **Python 3.10+**
- **Flask** – Backend API
- **Pillow (PIL)** – Image processing
- **Rembg** – Background removal (local, no API required)
- **Requests** & **Base64** – Frame data handling between backend and frontend

---

## Workflow Steps

### 1. Frame Extraction
- Key frames are extracted from the uploaded video using a custom `extract_key_frames` function.
- Each frame is encoded in Base64 format for processing.

### 2. Product Segmentation with Rembg
- Base64 frames are decoded and converted into image objects using **PIL**.
- The **Rembg** library removes the image background using the **U²-Net** model.
- The output is converted back into Base64 and stored in the response.

### 3. API Response Format
Example JSON response from the backend:
```json
{
  "segmented_images": [
    {
      "frame_index": 0,
      "segmented_image": "<base64_string>",
      "note": "Segmented successfully"
    }
  ]
}
```



Installation

Run the following commands to set up dependencies:

pip install rembg pillow

## AI Product Image Enhancement
### verview

This step focuses on enhancing the segmented product images extracted from YouTube video frames.
The goal was to generate 2–3 high-quality, studio-style product shots with professional backgrounds using AI-based image-to-image generation.

Initially, Gemini Nano and Gemini Flash were tested for image enhancement, but they did not support image generation.
Therefore, Stability AI’s Stable Diffusion XL model was used to achieve stable and high-quality results.

### Approach
1. Frame Extraction

Extracted key product frames from the YouTube video using FFmpeg.

Removed duplicates and blurry frames to retain only clear product views.

2. Segmentation

Used U²-Net (via Rembg) to remove the background and isolate the product from each frame.

3. Enhancement

Enhanced each segmented product using Stability AI’s Stable Diffusion XL model.

Generated 2–3 variations per product with realistic backgrounds (white studio, marble, wooden, or soft gradient).

Saved all enhanced images as base64 for frontend rendering.

Why Gemini Nano Could Not Be Used

Gemini Nano is an on-device text-only model, not accessible through Python SDK or API.

It does not include methods like generate_content() or generate_images().

This caused errors such as:

404 models/gemini-1.5-flash not found or not supported for generateContent


Gemini Nano and Gemini Flash are text-focused models, while Gemini 1.5 Pro supports full image generation.

Therefore, Stability AI’s API was used for reliable image-to-image enhancement.

API Integration

Endpoint:

https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image


Headers:

Authorization: Bearer STABILITY_API_KEY


Parameters Used:

init_image: Input segmented image (PNG)

image_strength: 0.35

text_prompts: "High-quality product photo on a clean white or marble background, soft lighting, subtle shadows."

steps: 30

samples: 2

Technologies Used

Backend: Python, Flask, Pillow, dotenv, requests

Frontend: React.js

Segmentation: Rembg (U²-Net)

Enhancement: Stability AI SDXL

### How to Run
Backend Setup
pip install -r requirements.txt
echo STABILITY_API_KEY=your_key > .env
python app.py

### Frontend Setup
cd client
npm install
npm run dev

### Challenges Faced

Gemini API limitations for image generation.

Occasional API timeouts (502 errors).

Maintaining product sharpness and lighting consistency after enhancement.

