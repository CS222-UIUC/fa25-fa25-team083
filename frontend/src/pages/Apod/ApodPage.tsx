import { useEffect, useState } from "react";
import ComponentCard from "../../components/common/ComponentCard";
import { getJSON } from "../../api/client";

export default function ApodPage() {
  const [data, setData] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    getJSON("/api/apod")
      .then((d) => {
        if (!mounted) return;
        setData(d);
      })
      .catch((e) => setError(String(e)));
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <div className="p-4">
      <ComponentCard title="NASA APOD">
        {error ? (
          <div className="text-sm text-red-500">{error}</div>
        ) : data ? (
          <div>
            {/* Render image or embed video when available. For YouTube links we convert to an embed URL so the video plays inline. */}
            {data.media_type === "image" && (
              <img src={data.url} alt={data.title} className="w-full rounded mb-3" />
            )}

            {data.media_type === "video" && (
              (() => {
                const url: string = data.url || "";

                // Try to derive a YouTube embed URL. Supports watch?v= and youtu.be short links.
                const ytMatch = url.match(/(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([A-Za-z0-9_-]{6,})/i);
                const embedUrl = ytMatch ? `https://www.youtube.com/embed/${ytMatch[1]}` : url;

                // Render responsive iframe; some providers may block embedding — fall back to an external link if needed.
                return (
                  <div className="mb-3" style={{ position: "relative", paddingBottom: "56.25%", height: 0 }}>
                    <iframe
                      title={data.title || "APOD video"}
                      src={embedUrl}
                      frameBorder={0}
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                      style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%" }}
                    />
                  </div>
                );
              })()
            )}
            <div className="font-medium">{data.title}</div>
            <div className="text-xs text-gray-500">Date: {data.date}</div>
            <p className="mt-2 text-sm text-gray-700">{data.explanation}</p>
          </div>
        ) : (
          <div className="text-sm text-gray-500">Loading…</div>
        )}
      </ComponentCard>
    </div>
  );
}
