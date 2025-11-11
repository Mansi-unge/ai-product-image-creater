# ==========================================
# app.py — AI Product Imagery Backend (LangGraph Node 3)
# ==========================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from nodes.extract_frames import extract_key_frames, analyze_with_gemini
from nodes.segment_product import segment_product_with_rembg
from nodes.enhance_products import enhance_product_images
import traceback

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (frontend <-> backend)

@app.route("/api/extract", methods=["POST"])
def extract_products():
    """
    Main API endpoint to process a YouTube video.

    Steps:
        1. Receive a video URL from the frontend.
        2. Extract key frames from the video.
        3. Analyze frames with Gemini to identify products.
        4. Segment main product with rembg.
        5. Enhance product images using Stability AI (free alternative to Replicate).
    """
    data = request.get_json()
    video_url = data.get("videoURL")

    if not video_url:
        return jsonify({"error": "Missing video URL"}), 400

    try:
        print(f" Received video URL: {video_url}")

        # Step  Extract frames
        frames = extract_key_frames(video_url)
        print(f" Extracted {len(frames)} key frames")

        # Step 2️ Analyze frames with Gemini
        products = analyze_with_gemini(frames)
        print(f" Gemini analysis complete. Found {len(products)} product mentions")

        # Step 3️ Segment products using rembg
        segmented = segment_product_with_rembg(frames)
        print(f" Segmented {len(segmented['segmented_images'])} product images")

        # Step 4️ Enhance products using Stability AI
        enhanced = enhance_product_images(segmented["segmented_images"])
        print(f" Generated {sum(len(e['enhancements']) for e in enhanced)} enhanced images")

        # Step 5️ Return all results as JSON
        return jsonify({
            "products": products,
            "segmented_images": segmented["segmented_images"],
            "enhanced_images": enhanced
        })

    except Exception as e:
        print(" Error occurred:\n", traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
