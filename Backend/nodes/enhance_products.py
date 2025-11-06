import base64
import io
import os
import time
from PIL import Image
from dotenv import load_dotenv
import requests

load_dotenv()
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

def enhance_product_images(segmented_images, num_enhancements=2):
    """
    Enhance segmented product images using Stability AI's Stable Image Edit API.
    Returns a list of enhanced base64 images.
    """
    enhanced_results = []
    stability_url = "https://api.stability.ai/v2beta/stable-image/edit"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "image/png"
    }

    for item in segmented_images:
        frame_index = item["frame_index"]
        segmented_b64 = item["segmented_image"]

        # Convert base64 to image
        img_data = base64.b64decode(segmented_b64)
        img = Image.open(io.BytesIO(img_data)).convert("RGB")

        temp_file = f"temp_{frame_index}.png"
        img.save(temp_file)

        enhanced_images_b64 = []
        prompt = "high-quality product photo on a clean white background, soft studio lighting, subtle shadows and reflections"

        for i in range(num_enhancements):
            try:
                with open(temp_file, "rb") as f:
                    for attempt in range(3):
                        response = requests.post(
                            stability_url,
                            headers=headers,
                            files={"image": ("input.png", f, "image/png")},
                            data={
                                "prompt": prompt,
                                "output_format": "png"
                            },
                        )

                        if response.status_code == 200:
                            enhanced_b64 = base64.b64encode(response.content).decode("utf-8")
                            enhanced_images_b64.append(enhanced_b64)
                            break
                        elif response.status_code == 502:
                            print(f"⚠️ Stability API 502 — retrying (frame {frame_index})...")
                            time.sleep(3)
                        else:
                            print(f"⚠️ Stability API error {response.status_code}: {response.text}")
                            break

            except Exception as e:
                print(f"⚠️ Enhancement failed for frame {frame_index}: {e}")

        # Clean up
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
