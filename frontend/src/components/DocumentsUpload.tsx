import React, { useState } from "react";
import API from "../utils/axiosInstance";

const DocumentsUpload = () => {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setPdfFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!pdfFile) return alert("Please select a file.");
    const formData = new FormData();
    formData.append("file", pdfFile);

    try {
      await API.post("/documents/upload-pdf/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      alert("✅ PDF uploaded successfully!");
    } catch (err) {
      console.error("❌ Upload error:", err);
      alert("PDF upload failed.");
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    try {
      setLoading(true);
      const res = await API.post<{ answer: string }>(
        "/documents/ask-pdf/",
        { question },
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      setAnswer(res.data.answer);
    } catch (err) {
      setAnswer("⚠️ Something went wrong.");
      console.error("❌ Ask error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Upload PDF */}
      <div className="bg-white dark:bg-gray-800 p-4 rounded shadow space-y-2">
        <h2 className="text-xl font-semibold">📄 Upload a PDF</h2>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button
          onClick={handleUpload}
          className="btn bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
        >
          Upload
        </button>
      </div>

      {/* Ask PDF */}
      <div className="bg-white dark:bg-gray-800 p-4 rounded shadow">
        <div className="flex items-center gap-2 border rounded px-3 py-2 bg-white dark:bg-gray-700">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            placeholder="Ask something about the uploaded PDF..."
            className="flex-grow focus:outline-none bg-transparent text-black dark:text-white"
          />
          <button
            onClick={handleAsk}
            disabled={loading}
            className="text-white bg-blue-600 hover:bg-blue-700 p-2 rounded"
          >
            {loading ? (
              <span className="text-sm">...</span>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            )}
          </button>
        </div>

        {answer && (
          <div className="mt-4 p-3 rounded bg-gray-100 dark:bg-gray-700 text-black dark:text-white">
            <strong>Answer:</strong> {answer}
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentsUpload;
