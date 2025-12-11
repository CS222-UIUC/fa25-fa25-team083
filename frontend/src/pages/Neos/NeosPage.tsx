import { useEffect, useState } from "react";
import ComponentCard from "../../components/common/ComponentCard";
import { getJSON } from "../../api/client";

export default function NeosPage() {
  const [data, setData] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    getJSON("/api/neos")
      .then((d) => {
        if (!mounted) return;
        setData(d);
      })
      .catch((e) => setError(String(e)));
    return () => {
      mounted = false;
    };
  }, []);

  if (error) return (
    <ComponentCard title="NEOs">
      <div className="text-sm text-red-500">{error}</div>
    </ComponentCard>
  );

  return (
    <div className="p-4">
      <ComponentCard title="NEOs (Near-Earth Objects)">
        {data ? (
          <div className="text-sm space-y-3">
            <div className="font-medium">NEOs Today: {data.element_count ?? 0}</div>

            <div className="space-y-2">
              {(Array.isArray(data.all_neos) && data.all_neos.length > 0) || (Array.isArray(data.closest_list) && data.closest_list.length > 0) ? (
                (data.all_neos ?? data.closest_list).map((n: any) => (
                  <div key={n.id} className="flex items-center justify-between text-xs text-gray-700">
                    <div className="truncate">
                      <div className="font-medium">{n.name || n.id}</div>
                      <div className="text-xs text-gray-500">Date: {n.close_date ?? '—'}</div>
                    </div>
                    <div className="text-right">
                      <div>{n.miss_distance_km != null ? `${Math.round(n.miss_distance_km).toLocaleString()} km` : '—'}</div>
                      <div className="text-xs text-gray-500">{n.velocity_km_s != null ? `${Number(n.velocity_km_s).toFixed(1)} km/s` : ''}</div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-xs text-gray-500">No NEOs for today</div>
              )}
            </div>

            </div>
          ) : (
            <div className="text-sm text-gray-500">Loading…</div>
          )}
      </ComponentCard>

      
    </div>
  );
}
