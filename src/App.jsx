import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { FaYoutube, FaSpinner } from "react-icons/fa";
import {
  AiOutlineCloudUpload,
  AiOutlineCheckCircle,
  AiOutlineWarning,
} from "react-icons/ai";

function App() {
  // -------------------- State Variables --------------------
  const [videoURL, setVideoURL] = useState(""); // YouTube video URL
  const [loading, setLoading] = useState(false); // Loading state
  const [response, setResponse] = useState(""); // API response message
  const [products, setProducts] = useState([]); // Extracted product frames
  const [segmentedImages, setSegmentedImages] = useState([]); // Segmented product images

  // -------------------- Helper Function --------------------
  const getYouTubeThumbnail = (url) => {
    try {
      const videoIdMatch = url.match(/(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|$)/);
      return videoIdMatch
        ? `https://img.youtube.com/vi/${videoIdMatch[1]}/hqdefault.jpg`
        : null;
    } catch {
      return null;
    }
  };

  const thumbnail = getYouTubeThumbnail(videoURL);

  // -------------------- Submit Handler --------------------
  const handleSubmit = async () => {
    if (!videoURL) {
      alert("Please enter a YouTube video URL!");
      return;
    }

    setLoading(true);
    setResponse("");
    setProducts([]);
    setSegmentedImages([]);

    try {
      const res = await axios.post("http://127.0.0.1:5000/api/extract", {
        videoURL: videoURL,
      });

      if (res.data.products) {
        // Safely parse description even if it contains ```json
        const parsedProducts = res.data.products.map((p) => {
          let cleanDesc = p.description
            .replace(/```json/g, "")
            .replace(/```/g, "")
            .trim();

          let productsList = [];
          try {
            productsList = JSON.parse(cleanDesc)?.products || [];
          } catch (err) {
            console.warn("Failed to parse product description:", err);
          }

          return {
            ...p,
            products: productsList,
          };
        });

        setProducts(parsedProducts);
        setResponse("✅ Product images extracted successfully!");
      } else {
        setResponse("⚠️ No products found in the video.");
      }

      if (res.data.segmented_images) {
        setSegmentedImages(res.data.segmented_images);
      }
    } catch (err) {
      console.error("Backend error:", err);
      setResponse(
        "❌ Backend error: " + (err.response?.data?.error || err.message)
      );
    } finally {
      setLoading(false);
    }
  };

  // -------------------- JSX Render --------------------
  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-linear-to-br from-indigo-100 via-white to-blue-200 p-6">
      <motion.div
        initial={{ opacity: 0, scale: 0.9, y: 40 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="backdrop-blur-lg bg-white/70 shadow-2xl rounded-3xl p-8 max-w-2xl w-full border border-white/40"
      >
        <h1 className="text-4xl font-extrabold text-center mb-6 flex items-center justify-center gap-3 text-gray-800 drop-shadow-sm">
          <FaYoutube className="text-red-600 text-8xl" />
          AI Product Image Extractor
        </h1>

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

        {thumbnail && (
          <motion.img
            src={thumbnail}
            alt="YouTube thumbnail"
            className="rounded-xl max-h-[360px] w-full mb-4 shadow-md hover:scale-[1.02] transition"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          />
        )}

        <motion.button
          whileHover={{ scale: loading ? 1 : 1.05 }}
          whileTap={{ scale: loading ? 1 : 0.97 }}
          onClick={handleSubmit}
          disabled={loading}
          className={`w-full flex items-center justify-center gap-2 py-3 rounded-xl text-white font-semibold transition-all duration-300 ${loading
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
                {/* <p className="text-sm text-gray-700">
                  <strong>Frame {p.frame_index}:</strong>{" "}
                  {p.products.length > 0
                    ? p.products.join(", ")
                    : "No products listed"}
                </p> */}
                <p className="text-sm text-gray-700">
                  <strong>Frame {p.frame_index}:</strong>{" "}
                  {p.products.length > 0
                    ? p.products.map(prod => prod.name).join(", ")
                    : "No products listed"}
                </p>

              </motion.div>
            ))}
          </div>
        )}

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
