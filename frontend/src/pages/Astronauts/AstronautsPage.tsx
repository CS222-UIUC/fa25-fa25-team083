import { useEffect, useState } from "react";
import ComponentCard from "../../components/common/ComponentCard";
import { getJSON } from "../../api/client";

export default function AstronautsPage() {
  const [data, setData] = useState<any[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    getJSON("/api/llspacedevs")
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
      <ComponentCard title="Astronaut Feed - Top Countries">
        {error ? (
          <div className="text-sm text-red-500">{error}</div>
        ) : data ? (
          <div className="text-sm space-y-4">
            {data.slice(0, 40).map((c: any, i: number) => (
              <div key={i} className="p-3 bg-gray-50 rounded-md">
                <div className="flex items-center justify-between">
                  <div className="font-medium">{c.country}</div>
                  <div className="text-xs text-gray-500">{c.count}</div>
                </div>

                {/* Names: support legacy array shape or { active, inactive } object shape */}
                <div className="mt-2 text-xs text-gray-700">
                  {Array.isArray(c.names) ? (
                    <div>{(c.names || []).join(', ')}</div>
                  ) : (
                    <div className="space-y-2">
                      {c.names?.active && c.names.active.length > 0 ? (
                        <div>
                          <div className="font-semibold">Active ({c.names.active.length})</div>
                          <div className="text-xs text-gray-700">{c.names.active.join(', ')}</div>
                        </div>
                      ) : null}

                      {c.names?.inactive && c.names.inactive.length > 0 ? (
                        <div>
                          <div className="font-semibold text-gray-500">Inactive ({c.names.inactive.length})</div>
                          <div className="text-xs text-gray-500">{c.names.inactive.join(', ')}</div>
                        </div>
                      ) : null}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-sm text-gray-500">Loading…</div>
        )}
      </ComponentCard>
    </div>
  );
}
