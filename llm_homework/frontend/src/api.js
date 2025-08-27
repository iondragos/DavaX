import axios from "axios";

const API_BASE = "http://localhost:8000";

export async function getRecommendation(prompt) {
  const res = await axios.post(`${API_BASE}/recommend`, { prompt });
  return res.data.response;
}

export async function generateImage(prompt) {
  const res = await axios.post(`${API_BASE}/image`, { prompt });
  return res.data.image_path;
}

export async function speak(prompt) {
  await axios.post(`${API_BASE}/speak`, { prompt });
}
