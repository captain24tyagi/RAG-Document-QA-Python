// src/services/api.js

import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

/**
 * Upload a .txt document to the backend for ingestion.
 * @param {File} file - The file object from <input type="file">
 * @returns {Promise<{ message, chunks_stored, new_chunks }>}
 */
export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${BASE_URL}/ingest`, formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });

  return response.data;
}

/**
 * Ask a question against the uploaded document.
 * @param {string} query - The user's question
 * @param {number} topK  - Number of chunks to retrieve (default 5)
 * @returns {Promise<{ answer, source_chunks }>}
 */
export async function askQuestion(query: string, topK = 5) {
  const response = await axios.post(`${BASE_URL}/ask`, {
    query,
    top_k: topK
  });

  return response.data;
}
