import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_URL,
  timeout: 120000,
});

export async function analyzeTicker(ticker: string) {
  const { data } = await api.post(`/analyze/${ticker}`);
  return data;
}

export async function chatWithAgent(ticker: string, message: string) {
  const { data } = await api.post(`/chat`, { ticker, message });
  return data;
}
