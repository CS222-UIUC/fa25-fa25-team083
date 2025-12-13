import { useEffect, useState } from "react";
import ComponentCard from "../../components/common/ComponentCard";
import { getJSON } from "../../api/client";

interface MoonPhaseData {
  phase: string;
  illumination: number;
  age: number;
  next_phase: string;
  days_to_next: number;
  date: string;
  rise?: string | null;
  set?: string | null;
  location?: { lat: number; lon: number };
  error?: string;
}

export default function MoonPhasePage() {
  const [data, setData] = useState<MoonPhaseData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [latitude, setLatitude] = useState<string>("40.7128"); // Default to NYC
  const [longitude, setLongitude] = useState<string>("-74.0060");

  const fetchMoonPhase = (lat?: string, lon?: string) => {
    let url = "/api/moon-phase";
    if (lat && lon) {
      url += `?lat=${lat}&lon=${lon}`;
    }
    getJSON(url)
      .then((d) => {
        setData(d);
        setError(null);
      })
      .catch((e) => {
        setError(String(e));
        setData(null);
      });
  };

  useEffect(() => {
    fetchMoonPhase(latitude, longitude);
  }, []);

  const getPhaseEmoji = (phase: string) => {
    switch (phase.toLowerCase()) {
      case "new moon":
        return "🌑";
      case "waxing crescent":
        return "🌒";
      case "first quarter":
        return "🌓";
      case "waxing gibbous":
        return "🌔";
      case "full moon":
        return "🌕";
      case "waning gibbous":
        return "🌖";
      case "last quarter":
        return "🌗";
      case "waning crescent":
        return "🌘";
      default:
        return "🌙";
    }
  };

  return (
    <div className="p-4">
      <ComponentCard title="Moon Phase Tracker">
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-3">Location Settings</h3>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Latitude
              </label>
              <input
                type="number"
                step="0.0001"
                value={latitude}
                onChange={(e) => setLatitude(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="40.7128"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Longitude
              </label>
              <input
                type="number"
                step="0.0001"
                value={longitude}
                onChange={(e) => setLongitude(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="-74.0060"
              />
            </div>
          </div>
          <button
            onClick={() => fetchMoonPhase(latitude, longitude)}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Update Location
          </button>
        </div>

        {error ? (
          <div className="text-sm text-red-500">{error}</div>
        ) : data ? (
          data.error ? (
            <div className="text-sm text-yellow-600 bg-yellow-50 p-3 rounded">
              {data.error}
            </div>
          ) : (
          <div className="space-y-4">
            <div className="text-center">
              <div className="text-6xl mb-2">{getPhaseEmoji(data.phase)}</div>
              <div className="text-2xl font-bold text-gray-800">{data.phase}</div>
              <div className="text-sm text-gray-600 mt-1">
                {data.illumination}% illuminated
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-6">
              <div className="bg-gray-50 p-3 rounded-lg">
                <div className="text-sm text-gray-600">Moon Age</div>
                <div className="text-lg font-semibold">{data.age} days</div>
              </div>
              <div className="bg-gray-50 p-3 rounded-lg">
                <div className="text-sm text-gray-600">Next Phase</div>
                <div className="text-lg font-semibold">{data.next_phase}</div>
              </div>
              {data.rise && (
                <div className="bg-gray-50 p-3 rounded-lg">
                  <div className="text-sm text-gray-600">Moon Rise</div>
                  <div className="text-lg font-semibold">
                    {new Date(data.rise).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              )}
              {data.set && (
                <div className="bg-gray-50 p-3 rounded-lg">
                  <div className="text-sm text-gray-600">Moon Set</div>
                  <div className="text-lg font-semibold">
                    {new Date(data.set).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              )}
            </div>

            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-sm text-blue-800">
                {data.days_to_next.toFixed(1)} days until {data.next_phase.toLowerCase()}
              </div>
            </div>

            <div className="mt-4">
              <div className="text-xs text-gray-500 text-center">
                Current as of {new Date(data.date).toLocaleDateString()}
              </div>
            </div>
          </div>
          )
        ) : (
          <div className="text-sm text-gray-500">Loading moon phase data…</div>
        )}
      </ComponentCard>
    </div>
  );
}