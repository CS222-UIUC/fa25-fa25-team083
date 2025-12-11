import { useEffect, useState } from "react";
import ComponentCard from "../../components/common/ComponentCard";
import { getJSON } from "../../api/client";

const fmt = (v: number | null | undefined, digits = 0) =>
  v == null ? "N/A" : (digits > 0 ? v.toFixed(digits) : Math.round(v).toString());

export default function MarsInsightPage() {
  const [data, setData] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    getJSON("/api/mars-insight")
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
      <ComponentCard title="Mars InSight">
        {error ? (
          <div className="text-sm text-red-500">{error}</div>
        ) : data ? (
          <div className="space-y-3">
            <div className="flex items-center">
              <div className="text-sm text-gray-600">Sol</div>
              <div className="text-sm font-medium text-gray-800" style={{ marginLeft: 10 }}>{data.sol}</div>
            </div>

            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              <div className="p-3 bg-gray-50 rounded-md">
                <div className="text-xs text-gray-500">Temperature (°C)</div>
                <div className="mt-2 text-sm font-semibold text-gray-800">Avg: {fmt(data.temp?.avg,1)}</div>
                <div className="mt-1 text-xs text-gray-500">Max: {fmt(data.temp?.max,1)}</div>
                <div className="text-xs text-gray-500">Min: {fmt(data.temp?.min,1)}</div>
              </div>

              <div className="p-3 bg-gray-50 rounded-md">
                <div className="text-xs text-gray-500">Wind (m/s)</div>
                <div className="mt-2 text-sm font-semibold text-gray-800">Avg: {fmt(data.wind?.avg,2)}</div>
                <div className="mt-1 text-xs text-gray-500">Max: {fmt(data.wind?.max,2)}</div>
                <div className="text-xs text-gray-500">Min: {fmt(data.wind?.min,2)}</div>
              </div>

              <div className="p-3 bg-gray-50 rounded-md">
                <div className="text-xs text-gray-500">Pressure (Pa)</div>
                <div className="mt-2 text-sm font-semibold text-gray-800">Avg: {fmt(data.pressure?.avg,0)}</div>
                <div className="mt-1 text-xs text-gray-500">Max: {fmt(data.pressure?.max,0)}</div>
                <div className="text-xs text-gray-500">Min: {fmt(data.pressure?.min,0)}</div>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-800 mt-2">7-sol history</h4>
              
              <div className="mt-2 p-3 bg-gray-50 rounded-md text-sm text-gray-700">
                {data.history && data.history.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="w-full text-left">
                      <thead>
                        <tr className="text-xs text-gray-500">
                          <th className="py-2">Sol</th>
                          <th className="py-2">Temp (°C)</th>
                          <th className="py-2">Wind (m/s)</th>
                          <th className="py-2">Pressure (Pa)</th>
                        </tr>
                      </thead>
                      <tbody>
                        {data.history.map((h: any) => (
                          <tr key={h.sol} className="align-top border-t border-gray-100">
                            <td className="py-2">Sol {h.sol}</td>
                            <td className="py-2">{fmt(h.temp?.avg, 1)}</td>
                            <td className="py-2">{fmt(h.wind?.avg, 2)}</td>
                            <td className="py-2">{fmt(h.pressure?.avg, 0)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="text-xs text-gray-500">No history</div>
                )}
              </div>
            </div>
          </div>
        ) : (
          <div className="text-sm text-gray-500">Loading…</div>
        )}
      </ComponentCard>
    </div>
  );
}
