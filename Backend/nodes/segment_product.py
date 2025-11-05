# Import necessary libraries
import base64  # To encode/decode images to/from base64 strings
import io  # To handle in-memory byte streams for images
import os  # For environment variables and file handling
from PIL import Image  # Python Imaging Library for opening and manipulating images
import google.generativeai as genai  # Google Gemini API

# Configure Gemini API with your API key stored in environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def segment_product_with_gemini(frames):
    """
    Use Google Gemini to segment (cut out) the main product from a set of frames.

    Args:
        frames (list): List of base64-encoded frames (images) to process.

    Returns:
        dict: Contains a list of dictionaries with the segmented image (base64) 
              and notes for each frame processed.
    """

    # Initialize the Gemini model specialized for image tasks
    model = genai.GenerativeModel("models/gemini-2.5-flash-image")

    # This list will store the output for each processed frame
    segmented_images = []

    # Process only the first 5 frames to save time and API usage
    for i, frame_b64 in enumerate(frames[:5]):
        # Decode the base64 image to bytes
        image_data = base64.b64decode(frame_b64)

        # Open the image from bytes using PIL
        img = Image.open(io.BytesIO(image_data))

        # Prompt to Gemini: instructs the model to segment the main product
        prompt = (
            "Segment the main product in this image. "
            "Return a cropped image of the product with transparent background. "
            "Focus on the product that appears most clearly."
        )

        try:
            # Send the image and prompt to Gemini
            response = model.generate_content([prompt, img])

            # Fallback: if Gemini does not return an image, keep original frame
            segmented_b64 = frame_b64
            note = getattr(response, "text", "Segmentation response received")

            # Check if the response contains image data
            if hasattr(response, "parts") and len(response.parts) > 0:
                part = response.parts[0]
                if hasattr(part, "data") and part.data:
                    segmented_b64 = part.data  # Replace with Gemini's segmented image
                    note = "Image output received"  # Update note

            # Append result for this frame
            segmented_images.append({
                "frame_index": i,  # Original frame index
                "segmented_image": segmented_b64,  # Base64 of segmented product
                "note": note  # Note about the response
            })

        except Exception as e:
            # If API fails, log the error but continue with other frames
            print(f"⚠️ Gemini segmentation failed on frame {i}: {e}")

    # Return all segmented images and their info
    return {"segmented_images": segmented_images}
