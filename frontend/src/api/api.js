import axios from "axios";

// Configure default base URL. Uses proxy in development, or container path in production.
const API = axios.create({
  baseURL: import.meta.env.PROD ? "" : "http://localhost:8000",
  timeout: 30000, // 30 second timeout for heavy HuggingFace BART/embedding runs
});

export const fetchManufacturerRankings = async () => {
  try {
    const response = await API.get("/api/manufacturers");
    return response.data;
  } catch (error) {
    console.error("Error fetching manufacturer rankings:", error);
    throw error;
  }
};

export const predictRecallSeverity = async (payload) => {
  try {
    const response = await API.post("/api/predict", payload);
    return response.data;
  } catch (error) {
    console.error("Error making recall prediction:", error);
    throw error;
  }
};

export const searchSemanticRecalls = async (query, topK = 6) => {
  try {
    const response = await API.post("/api/search", { query, top_k: topK });
    return response.data;
  } catch (error) {
    console.error("Error conducting semantic search:", error);
    throw error;
  }
};
