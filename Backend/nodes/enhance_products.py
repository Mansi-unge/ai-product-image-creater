import base64
import io
import os
import time
import random
from PIL import Image
from dotenv import load_dotenv
import requests

# Load Stability AI key
load_dotenv()
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

def enhance_product_images(segmented_images, num_enhancements=2):
    """
    Enhance product images using Stability AI Stable Diffusion XL with beautiful backgrounds.
    Each image enhancement uses a random high-quality background style.
    """
    enhanced_results = []
    stability_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image"
    headers = {"Authorization": f"Bearer {STABILITY_API_KEY}"}

    # Variety of beautiful backgrounds to randomize
    background_prompts = [
        "clean white background, soft studio lighting, subtle shadows",
        "luxury marble background, high-end lighting, studio shadows",
        "soft pastel gradient background, aesthetic and modern look",
        "wooden tabletop background with soft reflections and natural light",
        "minimal studio scene with smooth shadows and reflective floor",
        "light beige background, elegant minimalist e-commerce style",
        "abstract blurred background with soft lighting and bokeh effect"
    ]

    for item in segmented_images:
        frame_index = item["frame_index"]
        segmented_b64 = item["segmented_image"]

        # Decode base64 and prepare image
        img_data = base64.b64decode(segmented_b64)
        img = Image.open(io.BytesIO(img_data)).convert("RGB").resize((1024, 1024))

        # Resize if smaller than 512x512
        if img.width < 512 or img.height < 512:
            img = img.resize((512, 512))

        temp_file = f"temp_{frame_index}.png"
        img.save(temp_file)

        enhanced_images_b64 = []

        # Pick a random background prompt each time
        for i in range(num_enhancements):
            background = random.choice(background_prompts)
            prompt = f"high-quality product photo on a {background}, ultra-realistic, professional lighting, depth of field"

            try:
                with open(temp_file, "rb") as f:
                    files = {"init_image": (temp_file, f, "image/png")}
                    data = {
                        "init_image_mode": "IMAGE_STRENGTH",
                        "image_strength": 0.35,
                        "text_prompts[0][text]": prompt,
                        "text_prompts[0][weight]": 1,
                        "cfg_scale": 8,
                        "clip_guidance_preset": "FAST_BLUE",
                        "samples": 1,
                        "steps": 30
                    }

                    response = requests.post(stability_url, headers=headers, files=files, data=data)

                    if response.status_code == 200:
                        result = response.json()
                        enhanced_b64 = result["artifacts"][0]["base64"]
                        enhanced_images_b64.append(enhanced_b64)
                        print(f" Frame {frame_index} enhanced with background: {background}")
                    elif response.status_code == 502:
                        print(f"⚠ API 502 — retrying frame {frame_index}...")
                        time.sleep(3)
                    else:
                        print(f"⚠ API error {response.status_code}: {response.text}")

            except Exception as e:
                print(f"⚠ Enhancement failed for frame {frame_index}: {e}")

        # Clean temp file
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except PermissionError:
                pass

        enhanced_results.append({
            "frame_index": frame_index,
            "enhancements": enhanced_images_b64
        })

    return enhanced_results
