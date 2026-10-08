import { useState } from "react";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [context, setContext] = useState("");
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (event) => {
    const selectedImage = event.target.files[0];

    if (selectedImage) {
      setImage(selectedImage);
      setImagePreview(URL.createObjectURL(selectedImage));
      setResult(null);
      setMessage("");
    }
  };

  const handleAnalyze = async () => {
    if (!image) {
      setMessage("Please upload an incident image.");
      return;
    }

    if (!context.trim()) {
      setMessage("Please enter some incident context.");
      return;
    }

    setLoading(true);
    setMessage("");
    setResult(null);

    const formData = new FormData();

    formData.append("image", image);
    formData.append("context", context);

    try {
      const response = await fetch("http://127.0.0.1:8000/investigate", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed.");
      }

      setResult(data.evidence);
      setMessage("Incident analyzed successfully.");
    } catch (error) {
      console.error(error);
      setMessage(
        "Could not connect to the backend. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>AI WHAT WENT WRONG?</h1>

      <h2>Incident Detective</h2>

      <div className="upload-section">
        <label htmlFor="imageUpload" className="upload-button">
          Upload Incident Image
        </label>

        <input
          id="imageUpload"
          type="file"
          accept="image/*"
          onChange={handleImageChange}
        />
      </div>

      {imagePreview && (
        <div className="preview">
          <img src={imagePreview} alt="Incident Preview" />
        </div>
      )}

      <textarea
        placeholder="Context about the incident"
        rows="5"
        value={context}
        onChange={(event) => setContext(event.target.value)}
      />

      <button
        className="analyze-button"
        onClick={handleAnalyze}
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Analyze Incident"}
      </button>

      {message && <p>{message}</p>}

      {result && (
        <div className="result">
          <h2>Incident Evidence</h2>

          <h3>Visible Objects</h3>
          <ul>
            {result.visible_objects.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          <h3>Visible Conditions</h3>
          <ul>
            {result.visible_conditions.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          <h3>Evidence</h3>
          <ul>
            {result.evidence.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          <h3>Uncertainties</h3>
          <ul>
            {result.uncertainties.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;