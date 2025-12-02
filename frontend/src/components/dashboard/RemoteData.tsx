import React from "react";
import ComponentCard from "../common/ComponentCard";
import useDashboardData from "../../hooks/useDashboardData";

export default function RemoteData() {
  const { data, loading, error, refresh } = useDashboardData(60_000);

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
            <div className="text-xs">
              <pre className="overflow-auto max-h-48">{JSON.stringify(data.insight, null, 2)}</pre>
            </div>
          ) : (
            <div className="text-sm text-gray-500">No data</div>
          )}
        </ComponentCard>
      </div>

      <ComponentCard title="Timer / Launch Info">
        {data.countdown ? (
          <div className="text-sm">
            <div className="font-medium">{data.countdown.target_name}</div>
            <div className="text-xs text-gray-500">Target date: {data.countdown.target_date}</div>
            <div className="mt-2 grid grid-cols-4 gap-2">
              <div className="text-center">
                <div className="text-lg font-semibold">{data.countdown.days}</div>
                <div className="text-xs text-gray-500">Days</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{data.countdown.hours}</div>
                <div className="text-xs text-gray-500">Hours</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{data.countdown.minutes}</div>
                <div className="text-xs text-gray-500">Minutes</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold">{data.countdown.seconds}</div>
                <div className="text-xs text-gray-500">Seconds</div>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-sm text-gray-500">No data</div>
        )}
      </ComponentCard>
    </div>
  );
}
