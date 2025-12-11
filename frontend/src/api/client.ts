// backend Flask runs on port 8000 by default in `backend/app.py`
export const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getJSON(path: string) {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`GET ${url} failed: ${text}`);
  }
  return res.json();
}

export default {
  API_BASE,
  getJSON,
};
