import base64
import io
from PIL import Image
from rembg import remove

def segment_product_with_rembg(frames):
    """
    Segment main product from images using rembg (local, free).

    Args:
        frames (list): List of base64-encoded images.

    Returns:
        dict: Contains segmented images (base64) and notes.
    """
    segmented_images = []

    for i, frame_b64 in enumerate(frames):
        try:
            # Decode base64 image to bytes
            img_data = base64.b64decode(frame_b64)
            img = Image.open(io.BytesIO(img_data))

            # Remove background
            output = remove(img)  # returns PIL.Image with transparent background

            # Convert to base64
            buffered = io.BytesIO()
            output.save(buffered, format="PNG")
            segmented_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            segmented_images.append({
                "frame_index": i,
                "segmented_image": segmented_b64,
                "note": "Successfully segmented via rembg"
            })

        except Exception as e:
            print(f" rembg failed on frame {i}: {e}")
            segmented_images.append({
                "frame_index": i,
                "segmented_image": frame_b64,  # fallback to original
                "note": f"Segmentation failed: {e}"
            })

    return {"segmented_images": segmented_images}
