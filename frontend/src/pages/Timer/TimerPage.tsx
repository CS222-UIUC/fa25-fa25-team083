import { useEffect, useState } from "react";
import ComponentCard from "../../components/common/ComponentCard";
import { getJSON } from "../../api/client";

export default function TimerPage() {
  const [data, setData] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [live, setLive] = useState<null | { days: number; hours: number; minutes: number; seconds: number }>(null);

  useEffect(() => {
    let mounted = true;
    getJSON("/api/countdown")
      .then((d) => {
        if (!mounted) return;
        setData(d);
      })
      .catch((e) => setError(String(e)));
    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    if (!data?.target_date) {
      setLive(null);
      return;
    }

    const parseMs = (s: string) => {
      if (/[zZ]|[+\-][0-9]{2}:?[0-9]{2}$/.test(s)) return Date.parse(s);
      return Date.parse(s + "Z");
    };

    const target = parseMs(data.target_date);

    const tick = () => {
      const now = Date.now();
      let diff = Math.max(0, target - now);
      const days = Math.floor(diff / (24 * 3600 * 1000));
      diff %= 24 * 3600 * 1000;
      const hours = Math.floor(diff / (3600 * 1000));
      diff %= 3600 * 1000;
      const minutes = Math.floor(diff / (60 * 1000));
      diff %= 60 * 1000;
      const seconds = Math.floor(diff / 1000);
      setLive({ days, hours, minutes, seconds });
    };

    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [data?.target_date]);

  if (error) {
    return (
      <ComponentCard title="Timer / Launch Info">
        <div className="text-sm text-red-500">{error}</div>
      </ComponentCard>
    );
  }

  return (
    <div className="p-4">
      <ComponentCard title="Timer / Launch Info">
        {data ? (
          <div className="text-sm">
            <div className="font-medium">{data.target_name ?? "Countdown"}</div>
            <div className="text-xs text-gray-500">Target date: {data.target_date}</div>
            {live ? (
              <div className="mt-3 grid grid-cols-4 gap-2">
                <div className="text-center">
                  <div className="text-lg font-semibold">{live.days}</div>
                  <div className="text-xs text-gray-500">Days</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold">{live.hours}</div>
                  <div className="text-xs text-gray-500">Hours</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold">{live.minutes}</div>
                  <div className="text-xs text-gray-500">Minutes</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold">{live.seconds}</div>
                  <div className="text-xs text-gray-500">Seconds</div>
                </div>
              </div>
            ) : (
              <div className="mt-2 text-sm text-gray-500">No target date provided</div>
            )}
          </div>
        ) : (
          <div className="text-sm text-gray-500">Loading…</div>
        )}
      </ComponentCard>
    </div>
  );
}
