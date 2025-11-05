import { useState } from "react"; // React state hook
import axios from "axios"; // For HTTP requests
import { motion } from "framer-motion"; // For animations
import { FaYoutube, FaSpinner } from "react-icons/fa"; // YouTube and loading icons
import {
  AiOutlineCloudUpload,
  AiOutlineCheckCircle,
  AiOutlineWarning,
} from "react-icons/ai"; // Cloud upload, check, warning icons

function App() {
  // -------------------- State Variables --------------------
  const [videoURL, setVideoURL] = useState(""); // Store YouTube video URL input
  const [loading, setLoading] = useState(false); // Track API request loading state
  const [response, setResponse] = useState(""); // Store response message
  const [products, setProducts] = useState([]); // Store extracted product frames
  const [segmentedImages, setSegmentedImages] = useState([]); // Store segmented product images

  // -------------------- Helper Function --------------------
  const getYouTubeThumbnail = (url) => {
    // Extract video ID from URL and return YouTube thumbnail URL
    try {
      const videoIdMatch = url.match(/(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|$)/);
      return videoIdMatch
        ? `https://img.youtube.com/vi/${videoIdMatch[1]}/hqdefault.jpg`
        : null;
    } catch {
      return null;
    }
  };

  const thumbnail = getYouTubeThumbnail(videoURL); // Current video thumbnail

  // -------------------- Submit Handler --------------------
  const handleSubmit = async () => {
    if (!videoURL) {
      alert("Please enter a YouTube video URL!");
      return;
    }

    setLoading(true); // Start loading animation
    setResponse(""); // Clear previous messages
    setProducts([]); // Clear old extracted frames
    setSegmentedImages([]); // Clear old segmented images

    try {
      // POST request to Flask backend
      const res = await axios.post("http://127.0.0.1:5000/api/extract", {
        videoURL: videoURL,
      });

      // Set products if found
      if (res.data.products) {
        setProducts(res.data.products);
        setResponse("✅ Product images extracted successfully!");
      } else {
        setResponse("⚠️ No products found in the video.");
      }

      // Set segmented product images if returned
      if (res.data.segmented_images) {
        setSegmentedImages(res.data.segmented_images);
      }

    } catch (err) {
      console.error("Backend error:", err);
      setResponse(
        "❌ Backend error: " + (err.response?.data?.error || err.message)
      );
    } finally {
      setLoading(false); // Stop loading animation
    }
  };

  // -------------------- JSX Render --------------------
  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-linear-to-br from-indigo-100 via-white to-blue-200 p-6">
      {/* Main container with blurred background and rounded card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9, y: 40 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="backdrop-blur-lg bg-white/70 shadow-2xl rounded-3xl p-8 max-w-2xl w-full border border-white/40"
      >
        {/* Title */}
        <h1 className="text-4xl font-extrabold text-center mb-6 flex items-center justify-center gap-3 text-gray-800 drop-shadow-sm">
          <FaYoutube className="text-red-600 text-8xl" />
          AI Product Image Extractor
        </h1>

        {/* YouTube URL Input */}
        <div className="relative">
          <FaYoutube className="absolute left-3 top-3 text-gray-400 text-xl" />
          <input
            type="text"
            placeholder="Enter YouTube video URL"
            value={videoURL}
            onChange={(e) => setVideoURL(e.target.value)}
            className="w-full border border-gray-300/60 rounded-xl p-3 pl-10 mb-4 focus:outline-none focus:ring-4 focus:ring-blue-400/40 bg-white/80 backdrop-blur-sm shadow-sm"
          />
        </div>

        {/* YouTube Thumbnail Preview */}
        {thumbnail && (
          <motion.img
            src={thumbnail}
            alt="YouTube thumbnail"
            className="rounded-xl max-h-[360px] max-w-full mb-4 shadow-md hover:scale-[1.02] transition"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          />
        )}

        {/* Submit Button */}
        <motion.button
          whileHover={{ scale: loading ? 1 : 1.05 }}
          whileTap={{ scale: loading ? 1 : 0.97 }}
          onClick={handleSubmit}
          disabled={loading}
          className={`w-full flex items-center justify-center gap-2 py-3 rounded-xl text-white font-semibold transition-all duration-300 ${
            loading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-linear-to-br from-blue-500 to-indigo-600 hover:shadow-lg hover:from-indigo-500 hover:to-blue-600"
          }`}
        >
          {loading ? (
            <>
              <FaSpinner className="animate-spin text-lg" />
              Processing...
            </>
          ) : (
            <>
              <AiOutlineCloudUpload className="text-lg" />
              Extract Product Images
            </>
          )}
        </motion.button>

        {/* Response Message */}
        {response && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-5 flex items-center justify-center gap-2 text-gray-700 font-medium text-center"
          >
            {response.toLowerCase().includes("error") ? (
              <AiOutlineWarning className="text-red-500 text-xl" />
            ) : (
              <AiOutlineCheckCircle className="text-green-500 text-xl" />
            )}
            <span>{response}</span>
          </motion.div>
        )}

        {/* Display Extracted Product Frames */}
        {products.length > 0 && (
          <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
            {products.map((p, idx) => (
              <motion.div
                key={idx}
                className="bg-white/80 p-3 rounded-xl shadow-md border border-gray-200/60"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: idx * 0.1 }}
              >
                <img
                  src={`data:image/jpeg;base64,${p.frame}`}
                  alt={`Frame ${p.frame_index}`}
                  className="rounded-lg mb-2"
                />
                <p className="text-sm text-gray-700">
                  <strong>Frame {p.frame_index}:</strong> {p.description}
                </p>
              </motion.div>
            ))}
          </div>
        )}

        {/* Segmented Product Images Section */}
        {segmentedImages.length > 0 && (
          <div className="mt-8">
            <h2 className="text-xl font-bold mb-3">Segmented Product Images</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {segmentedImages.map((img, idx) => (
                <img
                  key={idx}
                  src={`data:image/png;base64,${img.segmented_image}`}
                  alt={`Segmented ${idx}`}
                  className="rounded-lg shadow-md"
                />
              ))}
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
}

export default App;
