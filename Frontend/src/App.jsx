import { useState } from "react";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [context, setContext] = useState("");
  const [message, setMessage] = useState("");

  const handleImageChange = (event) => {
    const selectedImage = event.target.files[0];

    if (selectedImage) {
      setImage(URL.createObjectURL(selectedImage));
    }
  };

  const handleAnalyze = () => {
  if (!image) {
    setMessage("Please upload an incident image.");
    return;
  }

  if (!context.trim()) {
    setMessage("Please enter some incident context.");
    return;
  }

  setMessage("Incident information is ready for analysis.");
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

      {image && (
        <div className="preview">
          <img src={image} alt="Incident Preview" />
        </div>
      )}

      <textarea
        placeholder="Context about the incident"
        rows="5"
        value={context}
        onChange={(event) => setContext(event.target.value)}
      ></textarea>

      <button className="analyze-button" onClick={handleAnalyze}>
  Analyze Incident
</button>
    </div>
  );
}

export default App;