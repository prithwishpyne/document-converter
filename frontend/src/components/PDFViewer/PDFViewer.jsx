import { useState, useRef } from "react";
import axios from "axios";
import styles from "./PDFViewer.module.css";

const PDFViewer = () => {
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fileInputRef = useRef(null);

  const handleUpload = async (event) => {
    setContent("");
    setLoading(true);
    setError(null);
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const response = await axios.post(
        "http://localhost:5000/api/pdf/upload",
        formData
      );
      setContent(response.data.content);
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.error || err.message);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className={styles.loading}>Loading content...</div>;
  }

  return (
    <div className={styles.pdfViewer}>
      <div className={styles.buttonContainer}>
        <button
          className={styles.viewButton}
          onClick={() => fileInputRef.current.click()}
        >
          Click to Upload and View PDF File
        </button>
        <input
          type="file"
          accept="application/pdf"
          onChange={handleUpload}
          hidden
          ref={fileInputRef}
        />
      </div>
      {error && <div className={styles.error}>{error}</div>}
      {content && (
        <div className={styles.content}>
          <div style={{ display: "flex", justifyContent: "end" }}>
            <button
              style={{
                background: "none",
                color: "#000",
                border: "1px solid #000",
              }}
              onClick={() => setContent("")}
            >
              Clear
            </button>
          </div>
          <>
            {content.split("\n").map((line, index) => {
              const isSectionHeader = /^\d+\.\s+[A-Z]+.*$/.test(line);
              const isSubsectionHeader = /^\s*\d+\.\s*\d+\.?\s+.*$/.test(line);

              const className = isSectionHeader
                ? styles.sectionHeader
                : isSubsectionHeader
                ? styles.subsectionHeader
                : styles.paragraph;

              return (
                <div key={index} className={className}>
                  {line}
                </div>
              );
            })}
          </>
        </div>
      )}
    </div>
  );
};

export default PDFViewer;
