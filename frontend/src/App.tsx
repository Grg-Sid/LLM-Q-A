import React, { useState } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./App.css";

export default function App(): JSX.Element {
  const [uploadResult, setUploadResult] = useState<string | undefined>();
  const [predictResult, setPredictResult] = useState<string | undefined>();
  const [file, setFile] = useState<File | null>(null);
  const [question, setQuestion] = useState<string>("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    const formData = new FormData();
    if (file) {
      formData.append("file", file);
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setUploadResult(response.data.result);
      toast.success("File uploaded successfully");
    } catch (error) {
      console.error("Error uploading file", error);
      toast.error("Failed to upload file");
    }
  };

  const handlePredict = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/predict?instruction=" + question);
      setPredictResult(response.data.result);
    } catch (error) {
      console.error("Error predicting", error);
      toast.error("Failed to predict");
    }
  };

  const resetForm = () => {
    setUploadResult(undefined);
    setPredictResult(undefined);
    setFile(null);
    setQuestion("");
  };

  return (
    <div className="appBlock">
      <div className="form">
        <h2>Upload File</h2>
        <input
          type="file"
          onChange={handleFileChange}
          className="fileInput"
          accept=".pdf, .docx, .txt"
          />
        <button onClick={handleUpload} disabled={!file}>
          Upload
        </button>
        {uploadResult && (
          <p className="resultOutput">Upload Result: {uploadResult}</p>
        )}
      </div>

      <div className="form">
        <h2>Predict</h2>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your question"
        />
        <button onClick={handlePredict} disabled={!question}>
          Predict
        </button>
        {predictResult && (
          <p className="resultOutput">Predict Result: {predictResult}</p>
        )}
      </div>

      <div className="form">
        <button onClick={resetForm} className="resetButton">
          Reset
        </button>
      </div>

      <ToastContainer />
    </div>
  );
}
