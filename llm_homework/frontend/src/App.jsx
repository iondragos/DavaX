import React, { useState } from 'react';
import { getRecommendation, generateImage, speak } from './api';

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [image, setImage] = useState(null);
  const [isRecording, setIsRecording] = useState(false);

  const handleSubmit = async () => {
    const res = await getRecommendation(prompt);
    setResponse(res);
    setImage(null);
  };

  const handleImage = async () => {
    const imgPath = await generateImage(prompt);
    setImage(`http://localhost:8000/${imgPath}`);
  };

  const handleSpeak = async () => {
    await speak(response);
  };

  const handleSpeechInput = () => {
      const recognition = new window.webkitSpeechRecognition() || new window.SpeechRecognition();

      recognition.lang = "en-US";
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onstart = () => {
        console.log("Listening...");
        setIsRecording(true);
      };

      recognition.onend = () => {
        setIsRecording(false);
      };

      recognition.onresult = (event) => {
        const spokenText = event.results[0][0].transcript;
        console.log("Transcribed:", spokenText);
        setPrompt(spokenText);
      };

      recognition.onerror = (event) => {
        console.error("Speech recognition error", event.error);
        alert("Could not transcribe. Try again.");
      };

      recognition.start();
  };


  return (
    <div
        style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            justifyContent: "flex-start",
            alignItems: "center",
            padding: "2rem",
            boxSizing: "border-box",
            backgroundColor: "inherit",
            color: "inherit",
            width: "100%",
        }}
    >
      <h1>📚 Smart Librarian</h1>

      <div style={{ display: "flex", gap: "10px", marginBottom: "20px", justifyContent: "center", width: "100%" }}>
          <input
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Ask for a book..."
             style={{
              flex: 1,
              padding: "14px 16px",
              fontSize: "18px",
              borderRadius: "8px",
              border: "1px solid #ccc",
              width: "200px",
              maxWidth: "40%",
            }}
          />
          <button
              onClick={handleSpeechInput}
              style={{
                padding: "14px 16px",
                backgroundColor: isRecording ? "green" : "",
                color: isRecording ? "white" : "",
                border: "1px solid #ccc",
                borderRadius: "8px"
              }}
          >
            🎤
          </button>
      </div>

      <div style={{ marginTop: 10, display: "flex", gap: "10px" }}>
        <button onClick={handleSubmit}>Recommend</button>
        <button onClick={handleSpeak} disabled={!response || response === "Inappropriate language!"}>Speak</button>
        <button onClick={handleImage} disabled={!response || response === "Inappropriate language!"}>Generate Image</button>
      </div>

      {response && !(response === "Inappropriate language!") && (
        <div style={{ marginTop: 20 }}>
            <h3>Recommendation:</h3>
            <p style={{ maxWidth: "900px", margin: "0 auto", lineHeight: "1.6" }}>
                {response}
            </p>
        </div>
      )}

      {response && response === "Inappropriate language!" && (
        <div style={{ marginTop: 20, color: "red" }}>
            <h3>ERROR</h3>
            <p>{response}</p>
        </div>
      )}


      {image && (
        <div style={{ marginTop: 20 }}>
          <h3>Generated Image:</h3>
          <img src={image} alt="Book Visual" style={{ width: "100%" }} />
        </div>
      )}
    </div>
  );
}

export default App;
