# Import necessary libraries
import cv2  # OpenCV for video processing
import base64  # For encoding frames into base64
import google.generativeai as genai  # Google Gemini API
import io  # To handle in-memory byte streams
import os  # For file and directory operations
from dotenv import load_dotenv  # To load environment variables from a .env file
from PIL import Image  # Python Imaging Library, for image manipulation
import yt_dlp  # Library to download videos from YouTube

# Load API key from .env file and configure Gemini API
load_dotenv()  # Loads environment variables from a .env file in the project root
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Configure Gemini API with your API key


def download_youtube_video(video_url):
    """
    Download a YouTube video using yt_dlp.
    
    Args:
        video_url (str): The URL of the YouTube video.
    
    Returns:
        str: Local file path to the downloaded video.
    """
    # Ensure the "downloads" folder exists
    os.makedirs("downloads", exist_ok=True)

    # yt_dlp options
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",  # Get best quality video+audio
        "merge_output_format": "mp4",  # Merge video and audio into MP4
        "outtmpl": "downloads/%(title)s.%(ext)s",  # Save filename as the video's title
        "quiet": False,  # Show download logs
        "noprogress": False,  # Show progress bar
        "extractor_args": {"youtube": {"player_client": ["android"]}},  # Solve certain YouTube access issues
    }

    try:
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)  # Download and get metadata
            video_path = ydl.prepare_filename(info)  # Get local path to downloaded file
            return video_path
    except Exception as e:
        print(f"yt_dlp download failed: {e}")
        raise ValueError("Could not download YouTube video.")


def extract_key_frames(video_url, interval=5):
    """
    Extract key frames from the video at a specified interval.
    
    Args:
        video_url (str): URL of the YouTube video.
        interval (int): Seconds between each extracted frame.
    
    Returns:
        list: Base64-encoded frames.
    """
    # Download video first
    video_path = download_youtube_video(video_url)
    
    # Open video using OpenCV
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    # Get frames per second (fps) to calculate frame intervals
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    frames = []  # List to store base64-encoded frames
    count = 0

    # Loop through each frame in the video
    while True:
        ret, frame = cap.read()  # Read frame
        if not ret:
            break  # End of video

        # Select frames at regular intervals (e.g., every 'interval' seconds)
        if count % (fps * interval) == 0:
            _, buffer = cv2.imencode(".jpg", frame)  # Encode frame as JPEG
            frame_b64 = base64.b64encode(buffer).decode("utf-8")  # Convert to base64
            frames.append(frame_b64)

        count += 1

    cap.release()  # Release video file
    print(f" Extracted {len(frames)} key frames")
    return frames


def analyze_with_gemini(frames):
    """
    Analyze frames using Google Gemini to detect and describe products.
    
    Args:
        frames (list): List of base64-encoded frames.
    
    Returns:
        list: List of dictionaries containing frame index, frame, and Gemini analysis.
    """
    # Initialize Gemini model
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    
    products = []

    # Limit processing to first 5 frames for efficiency
    for i, frame_b64 in enumerate(frames[:5]):
        image_bytes = base64.b64decode(frame_b64)  # Decode base64 back to bytes
        img = Image.open(io.BytesIO(image_bytes))  # Open image from bytes

        # Prompt to Gemini API
        prompt = """
        Analyze this frame from a product video.
        Identify any products shown and describe them briefly.
        Output in strict JSON format:
        {
          "products": [
            {"name": "Product Name", "description": "Short description"}
          ]
        }
        """

        try:
            # Generate content using Gemini
            response = model.generate_content([prompt, img])
            products.append({
                "frame_index": i,  # Frame number
                "frame": frame_b64,  # Base64 image
                "description": response.text.strip()  # Gemini's response
            })
        except Exception as e:
            print(f" Gemini API failed on frame {i}: {e}")

    print(f" Processed {len(products)} frames with Gemini")
    return products
