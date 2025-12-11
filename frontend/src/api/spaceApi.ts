const BASE_URL = "http://localhost:8000";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

export function fetchApod() {
  return get<{
    date: string;
    title: string;
    explanation: string;
    media_type: string;
    url: string;
  }>("/api/apod");
}

export function fetchMarsInsight() {
  return get<any>("/api/mars-insight");
}

export function fetchCountdown() {
  return get<any>("/api/countdown");
}
