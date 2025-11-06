Step 7 – AI Product Image Enhancement
Overview

This step focuses on enhancing the segmented product images extracted from YouTube video frames. The goal was to generate 2–3 high-quality, studio-style product shots with professional backgrounds using AI-based image-to-image generation.

Initially, Gemini Nano and Gemini Flash were tested for image enhancement, but they did not support image generation. Therefore, Stability AI’s Stable Diffusion XL model was used to achieve successful and high-quality results.

Approach

Frame Extraction
Extracted key product frames from the YouTube video using FFmpeg, removing duplicates and blurry frames.

Segmentation
Used U²-Net (via Rembg) to remove the background and isolate the product from each frame.

Enhancement

Enhanced each segmented product using Stability AI’s Stable Diffusion XL model.

Generated 2–3 variations for each product with realistic backgrounds (white studio, marble, wooden, or soft gradient styles).

Saved enhanced images as base64 for frontend display.

Why Gemini Nano Could Not Be Used

Gemini Nano is an on-device text-only model, not accessible through Python SDK or API.

It does not include methods like generate_content() or generate_images().

This caused errors such as:

404 models/gemini-1.5-flash not found or not supported for generateContent


Nano and Flash are text-focused models, while Gemini 1.5 Pro supports full image generation.

Therefore, Stability AI’s API was chosen for reliable image-to-image enhancement.

API Integration

Endpoint:

https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image


Headers:

Authorization: Bearer STABILITY_API_KEY


Parameters Used:

init_image: Input segmented image (PNG)

image_strength: 0.35

text_prompts: “High-quality product photo on a clean white or marble background, soft lighting, subtle shadows.”

steps: 30

samples: 2

Technologies Used

Backend: Python, Flask, Pillow, dotenv, requests

Frontend: React.js

Segmentation: Rembg (U²-Net)

Enhancement: Stability AI SDXL

How to Run

Backend Setup

pip install -r requirements.txt
echo STABILITY_API_KEY=your_key > .env
python app.py


Frontend Setup

cd client
npm install
npm run dev

Challenges Faced

Gemini API limitations for image generation.

Occasional API timeouts (502 errors).

Maintaining product sharpness after resizing.

Improvements

Allow users to select background styles.

Add caching for repeated image enhancements.

Use async queues for processing longer videos efficiently.
