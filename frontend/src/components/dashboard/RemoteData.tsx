import React, { useEffect, useState } from "react";
import ComponentCard from "../common/ComponentCard";
import useDashboardData from "../../hooks/useDashboardData";

export default function RemoteData() {
  const { data, loading, error, refresh } = useDashboardData(60_000);
  // temp chart removed — display numeric values for current sol instead

  // Live countdown state — derived from data.countdown.target_date and updated every second
  const [liveCountdown, setLiveCountdown] = useState<null | {
    days: number;
    hours: number;
    minutes: number;
    seconds: number;
    target_name?: string;
    target_date?: string;
  }>(null);

  useEffect(() => {
    const targetDateStr = data.countdown?.target_date;
    if (!targetDateStr) {
      setLiveCountdown(null);
      return;
    }

    // parse target date: if no timezone present, assume UTC and append 'Z'
    const parseMs = (s: string) => {
      if (/[zZ]|[+\-][0-9]{2}:?[0-9]{2}$/.test(s)) return Date.parse(s);
      return Date.parse(s + "Z");
    };

    const targetMs = parseMs(targetDateStr);

    const tick = () => {
      const now = Date.now();
      let diff = Math.max(0, targetMs - now);
      const days = Math.floor(diff / (24 * 3600 * 1000));
      diff %= 24 * 3600 * 1000;
      const hours = Math.floor(diff / (3600 * 1000));
      diff %= 3600 * 1000;
      const minutes = Math.floor(diff / (60 * 1000));
      diff %= 60 * 1000;
      const seconds = Math.floor(diff / 1000);
      setLiveCountdown({
        days,
        hours,
        minutes,
        seconds,
        target_name: data.countdown?.target_name,
        target_date: data.countdown?.target_date,
      });
    };

    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data.countdown?.target_date]);

  // helper to format numeric -> string; show "N/A" when value is null/undefined
  const fmt = (v: number | null | undefined, digits = 0) =>
    v == null ? "N/A" : (digits > 0 ? v.toFixed(digits) : Math.round(v).toString());

  // ...existing code...

  // small history mini-bars rendering
  const renderHistory = (history: any[] | undefined) => {
    if (!history || history.length === 0)
      return <div className="text-sm text-gray-500">No history</div>;

    // show most recent sol first in the UI: sort by sol numeric descending
    const sorted = history.slice().sort((a: any, b: any) => {
      const ai = parseInt(String(a?.sol ?? ""), 10);
      const bi = parseInt(String(b?.sol ?? ""), 10);
      if (Number.isNaN(ai) || Number.isNaN(bi)) return 0;
      return bi - ai;
    });

    // compute min/max per metric among available non-null values
    const extract = (keyPath: string) =>
      sorted.map((h: any) => {
        const parts = keyPath.split(".");
        let cur: any = h;
        for (const p of parts) {
          cur = cur?.[p];
          if (cur == null) break;
        }
        return cur ?? null;
      });

    const temps = extract("temp.avg").filter((v: number | null) => v != null) as number[];
    const winds = extract("wind.avg").filter((v: number | null) => v != null) as number[];
    const presses = extract("pressure.avg").filter((v: number | null) => v != null) as number[];

    const minMax = (arr: number[]) =>
      arr.length === 0 ? [0, 1] : [Math.min(...arr), Math.max(...arr) || Math.min(...arr) + 1];

    const [tmin, tmax] = minMax(temps);
    const [wmin, wmax] = minMax(winds);
    const [pmin, pmax] = minMax(presses);

    const pct = (v: number | null, min: number, max: number) => {
      if (v == null) return 0;
      if (max === min) return 50;
      return Math.max(2, Math.min(100, ((v - min) / (max - min)) * 100));
    };

    return (
      <div className="space-y-2 text-sm">
        <div className="flex items-center text-xs text-gray-500 justify-between">
          <div className="w-1/4">Sol</div>
          <div className="w-3/4 grid grid-cols-3 gap-2">
            <div className="text-left pl-2">Temp (°C)</div>
            <div className="text-left pl-2" style={{ paddingLeft: "2px" }}>Wind (m/s)</div>
            <div className="text-right pr-10 whitespace-nowrap">Pressure (Pa)</div>
          </div>
        </div>

        {sorted.map((h: any) => (
          <div key={h.sol} className="flex items-center gap-2">
            <div className="w-1/4 text-xs text-gray-600">{h.sol}</div>

            <div className="w-3/4 grid grid-cols-3 gap-2 items-center">
              {/* Temp bar */}
              <div className="flex items-center gap-2">
                <div className="w-full h-2 bg-gray-200 rounded overflow-hidden">
                  <div
                    className="h-2 bg-red-400 rounded"
                    style={{ width: `${pct(h?.temp?.avg ?? null, tmin, tmax)}%` }}
                  />
                </div>
                <div className="w-12 text-xs text-right text-gray-700">{fmt(h?.temp?.avg, 1)}</div>
              </div>

              {/* Wind bar */}
              <div className="flex items-center gap-2">
                <div className="w-full h-2 bg-gray-200 rounded overflow-hidden">
                  <div
                    className="h-2 bg-indigo-400 rounded"
                    style={{ width: `${pct(h?.wind?.avg ?? null, wmin, wmax)}%` }}
                  />
                </div>
                <div className="w-12 text-xs text-right text-gray-700">{fmt(h?.wind?.avg, 2)}</div>
              </div>

              {/* Pressure bar */}
              <div className="flex items-center gap-2">
                <div className="w-full h-2 bg-gray-200 rounded overflow-hidden">
                  <div
                    className="h-2 bg-green-400 rounded"
                    style={{ width: `${pct(h?.pressure?.avg ?? null, pmin, pmax)}%` }}
                  />
                </div>
                <div className="w-12 text-xs text-right text-gray-700">{fmt(h?.pressure?.avg, 0)}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
          Live NASA & External Endpoints
        </h3>
        <div className="flex items-center gap-2">
          <button
            onClick={() => refresh()}
            className="inline-flex items-center px-3 py-1.5 rounded-md bg-gray-100 text-sm text-gray-700 hover:bg-gray-200"
          >
            Refresh
          </button>
          {loading && <span className="text-theme-sm text-gray-500">Updating…</span>}
        </div>
      </div>

      {error ? (
        <ComponentCard title="Error">
          <div className="text-sm text-red-500">{error}</div>
        </ComponentCard>
      ) : null}

      <ComponentCard title="Timer / Launch Info">
        {(liveCountdown || data.countdown) ? (
          (() => {
            const c = liveCountdown || data.countdown;
            const days = c.days ?? 0;
            const hours = c.hours ?? 0;
            const minutes = c.minutes ?? 0;
            const seconds = c.seconds ?? 0;
            const name = (c as any).target_name ?? (data.countdown && (data.countdown as any).target_name) ?? "Countdown";
            const date = (c as any).target_date ?? (data.countdown && (data.countdown as any).target_date) ?? "";
            return (
              <div className="text-sm">
                <div className="font-medium">{name}</div>
                <div className="text-xs text-gray-500">Target date: {date}</div>
                <div className="mt-2 grid grid-cols-4 gap-2">
                  <div className="text-center">
                    <div className="text-lg font-semibold">{days}</div>
                    <div className="text-xs text-gray-500">Days</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-semibold">{hours}</div>
                    <div className="text-xs text-gray-500">Hours</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-semibold">{minutes}</div>
                    <div className="text-xs text-gray-500">Minutes</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-semibold">{seconds}</div>
                    <div className="text-xs text-gray-500">Seconds</div>
                  </div>
                </div>
              </div>
            );
          })()
        ) : (
          <div className="text-sm text-gray-500">No data</div>
        )}
      </ComponentCard>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <ComponentCard title="NASA APOD">
          {data.apod ? (
            <div>
              {data.apod.media_type === "image" && (
                <img src={data.apod.url} alt={data.apod.title} className="w-full rounded mb-2" />
              )}
              <div className="font-medium">{data.apod.title}</div>
              <p className="mt-2 text-sm text-gray-500 line-clamp-4">{data.apod.explanation}</p>
              <div className="mt-2 text-xs text-gray-400">Date: {data.apod.date}</div>
            </div>
          ) : (
            <div className="text-sm text-gray-500">No data</div>
          )}
        </ComponentCard>
        <ComponentCard title="Mars InSight">
          {data.insight ? (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="text-sm text-gray-600">Sol</div>
                <div className="text-sm font-medium text-gray-800">{data.insight.sol}</div>
              </div>

              <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
                {/* Temperature with small bar chart */}
                <div className="p-3 bg-gray-50 rounded-md">
                    <div className="text-xs text-gray-500">Temperature (°C)</div>
                      <div className="mt-2 text-sm font-semibold text-gray-800">Avg: {data.insight.temp?.avg != null ? data.insight.temp.avg.toFixed(1) : "N/A"}</div>
                      <div className="mt-1 text-xs text-gray-500">Max: {data.insight.temp?.max != null ? data.insight.temp.max.toFixed(1) : "N/A"}</div>
                      <div className="text-xs text-gray-500">Min: {data.insight.temp?.min != null ? data.insight.temp.min.toFixed(1) : "N/A"}</div>
                </div>

                {/* Wind */}
                <div className="p-3 bg-gray-50 rounded-md">
                  <div className="text-xs text-gray-500">Wind (m/s)</div>
                    <div className="mt-2 text-sm font-semibold text-gray-800">Avg: {data.insight.wind?.avg != null ? data.insight.wind.avg.toFixed(2) : "N/A"}</div>
                    <div className="mt-1 text-xs text-gray-500">Max: {data.insight.wind?.max != null ? data.insight.wind.max.toFixed(2) : "N/A"}</div>
                    <div className="text-xs text-gray-500">Min: {data.insight.wind?.min != null ? data.insight.wind.min.toFixed(2) : "N/A"}</div>
                </div>

                {/* Pressure */}
                <div className="p-3 bg-gray-50 rounded-md">
                  <div className="text-xs text-gray-500">Pressure (Pa)</div>
                    <div className="mt-2 text-sm font-semibold text-gray-800">Avg: {data.insight.pressure?.avg != null ? data.insight.pressure.avg.toFixed(0) : "N/A"}</div>
                    <div className="mt-1 text-xs text-gray-500">Max: {data.insight.pressure?.max != null ? data.insight.pressure.max.toFixed(0) : "N/A"}</div>
                    <div className="text-xs text-gray-500">Min: {data.insight.pressure?.min != null ? data.insight.pressure.min.toFixed(0) : "N/A"}</div>
                </div>
              </div>

              {/* 7-sol history */}
              <div>
                <h4 className="text-sm font-medium text-gray-800 mt-2">7-sol history</h4>
                <div className="mt-2 p-3 bg-gray-50 rounded-md">
                  {renderHistory(data.insight.history)}
                </div>
              </div>

              {/* raw JSON removed for cleaner UI */}
            </div>
          ) : (
            <div className="text-sm text-gray-500">No data</div>
          )}
        </ComponentCard>
        <ComponentCard title="NEOs (Near-Earth Objects)">
          {data.neos ? (
            <div className="space-y-2 text-sm">
              <div className="flex items-center justify-between">
                <div className="font-medium">NEOs Today: {data.neos.element_count ?? 0}</div>
                <div className="text-right text-xs text-gray-500">
                  <div>Distance (km)</div>
                  <div>Speed (km/s)</div>
                </div>
              </div>

              {/* Closest object summary */}
              {/* Top 5 closest NEOs (closest -> farthest) */}
              {Array.isArray(data.neos.closest_list) && data.neos.closest_list.length > 0 ? (
                <div className="space-y-2">
                  {data.neos.closest_list.slice(0, 5).map((n: any) => (
                    <div key={n.id} className="flex items-center justify-between text-xs text-gray-700">
                      <div className="truncate">
                        <div className="font-medium">{n.name || n.id || "Unnamed"}</div>
                        <div className="text-xs text-gray-500">Date: {n.close_date ?? "—"}</div>
                      </div>
                      <div className="text-right">
                        <div>{n.miss_distance_km != null ? `${Math.round(n.miss_distance_km).toLocaleString()} km` : "—"}</div>
                        <div className="text-xs text-gray-500">{n.velocity_km_s != null ? `${Number(n.velocity_km_s).toFixed(1)} km/s` : ""}</div>
                        <div className="mt-1 text-xs text-gray-500">&nbsp;</div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-xs text-gray-600">Closest: —</div>
              )}

              {/* Largest object summary */}
              {data.neos.largest ? (
                <div className="text-xs text-gray-600">
                  <div className="font-semibold">Largest: {data.neos.largest.name ?? "Unnamed"}</div>
                  <div className="text-xs">Estimated max diameter: {data.neos.largest.max_diameter_m != null ? `${Math.round(data.neos.largest.max_diameter_m)} m` : "—"}</div>
                  <div className="mt-2 text-xs text-gray-500">&nbsp;</div>
                </div>
              ) : null}
            </div>
          ) : (
            <div className="text-sm text-gray-500">No data</div>
          )}
        </ComponentCard>
      </div>

      <ComponentCard title="LLSpaceDevs - Top Countries">
        {data.llspacedevs ? (
          <div className="text-sm">
            <ul className="space-y-2">
              {Array.isArray(data.llspacedevs) && data.llspacedevs.length > 0 ? (
                data.llspacedevs.slice(0, 6).map((c: any, i: number) => (
                  <li key={i} className="flex justify-between">
                    <span className="truncate">{c.country}</span>
                    <span className="font-medium text-gray-700">{c.count}</span>
                  </li>
                ))
              ) : (
                <li className="text-xs text-gray-500">No summary available</li>
              )}
            </ul>
            <details className="mt-2 text-xs text-gray-500">
              <summary className="cursor-pointer">Show names</summary>
              <div className="mt-2">
                {Array.isArray(data.llspacedevs) && data.llspacedevs.length > 0 ? (
                  data.llspacedevs.slice(0, 6).map((c: any, i: number) => (
                    <div key={i} className="mb-2">
                      <div className="text-xs font-semibold">{c.country} ({c.count})</div>
                      <div className="text-xs text-gray-600">{(c.names || []).slice(0,5).join(', ')}</div>
                    </div>
                  ))
                ) : null}
              </div>
            </details>
          </div>
        ) : (
          <div className="text-sm text-gray-500">No data</div>
        )}
      </ComponentCard>
    </div>
  );
}
