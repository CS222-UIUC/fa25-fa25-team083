import { useEffect, useRef, useState } from "react";
import { getJSON } from "../api/client";

export type DashboardData = {
  apod: any | null;
  insight: any | null;
  countdown: any | null;
};

export function useDashboardData(pollIntervalMs = 60_000) {
  const [data, setData] = useState<DashboardData>({
    apod: null,
    insight: null,
    countdown: null,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const mounted = useRef(true);

  const fetchAll = async () => {
    setLoading(true);
    setError(null);
    try {
      const [apod, insight, countdown] = await Promise.all([
        // backend routes from backend/app.py
        getJSON("/api/apod"),
        getJSON("/api/mars-insight"),
        getJSON("/api/countdown"),
      ]);
      if (!mounted.current) return;
      setData({ apod, insight, countdown });
    } catch (err: any) {
      if (!mounted.current) return;
      setError(err?.message || String(err));
    } finally {
      if (mounted.current) setLoading(false);
    }
  };

  useEffect(() => {
    mounted.current = true;
    fetchAll();
    const t = setInterval(fetchAll, pollIntervalMs);
    return () => {
      mounted.current = false;
      clearInterval(t);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pollIntervalMs]);

  return { data, loading, error, refresh: fetchAll };
}

export default useDashboardData;
