# Import necessary libraries
from flask import Flask, request, jsonify  # Flask framework for API creation
from flask_cors import CORS  # To allow cross-origin requests (frontend <-> backend)
from nodes.extract_frames import extract_key_frames, analyze_with_gemini  # Custom functions for frame extraction & analysis
from nodes.segment_product import segment_product_with_gemini  # Custom function for product segmentation
import traceback  # For detailed error logging

# Initialize Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
# This allows frontend apps (e.g., React) hosted on different ports/domains to access this API
CORS(app)

@app.route("/api/extract", methods=["POST"])
def extract_products():
    """
    Main API endpoint to process a YouTube video.
    
    Steps:
        1. Receive a video URL from the frontend.
        2. Extract key frames from the video.
        3. Analyze frames with Gemini to identify products.
        4. Segment the main product from the frames.
        5. Return the product info and segmented images as JSON.
    """

    # Parse JSON data from request
    data = request.get_json()
    video_url = data.get("videoURL")  # Expecting a key "videoURL" in request body

    # Validate input
    if not video_url:
        return jsonify({"error": "Missing video URL"}), 400

    try:
        print(f"Received video URL: {video_url}")

        # 1️⃣ Extract key frames from the video
        frames = extract_key_frames(video_url)
        # Optional debug: print(f"✅ Extracted {len(frames)} frames")

        # 2️⃣ Analyze frames with Gemini to identify products
        products = analyze_with_gemini(frames)
        # Optional debug: print(f"✅ Gemini analysis complete. Found {len(products)} results")

        # 3️⃣ Segment the main product from the frames using Gemini
        segmented = segment_product_with_gemini(frames)

        # Return all results as JSON
        return jsonify({
            "products": products,  # Analysis results
            "segmented_images": segmented["segmented_images"]  # Segmented product images
        })

    except Exception as e:
        # Log the full traceback for debugging
        print("❌ Error occurred:\n", traceback.format_exc())
        # Return error as JSON
        return jsonify({"error": str(e)}), 500


# Run Flask app on port 5000 in debug mode
if __name__ == "__main__":
    app.run(port=5000, debug=True)
