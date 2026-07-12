import { useState } from "react";
import useDashboard from "../hooks/useDashboard";

export default function Websites() {
  const { data, isLoading, isError, refetch } = useDashboard();
  const [checking, setChecking] = useState(false);

  const health = data?.health;

  async function handleCheckNow() {
  setChecking(true);

  try {
    await fetch("http://127.0.0.1:5001/health-check");
    await refetch();
  } finally {
    setChecking(false);
  }
}

  if (isLoading) {
    return <p className="text-slate-500">Loading website status...</p>;
  }

  if (isError) {
    return <p className="text-red-600">Website monitoring failed.</p>;
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-900">
          Website Monitor
        </h1>

        <p className="mt-1 text-slate-500">
          Monitor website uptime and response time
        </p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col justify-between gap-5 md:flex-row md:items-center">
          <div>
            <p className="text-sm text-slate-500">Monitored Website</p>

            <h2 className="mt-1 text-xl font-semibold text-slate-900">
              {health?.url || "Website URL unavailable"}
            </h2>

            <div className="mt-4 flex flex-wrap gap-3">
              <span
                className={`rounded-full px-3 py-1 text-sm font-semibold ${
                  health?.status === "up"
                    ? "bg-green-100 text-green-700"
                    : health?.status === "slow"
                    ? "bg-amber-100 text-amber-700"
                    : "bg-red-100 text-red-700"
                }`}
              >
                {health?.status?.toUpperCase() || "UNKNOWN"}
              </span>

              <span className="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700">
                Response: {health?.response_time_seconds ?? 0} sec
              </span>

              <span className="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700">
                HTTP: {health?.status_code ?? "N/A"}
              </span>
            </div>
          </div>

          <button
            onClick={handleCheckNow}
            disabled={checking}
            className="rounded-xl bg-blue-600 px-5 py-3 font-medium text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {checking ? "Checking..." : "Check Now"}
          </button>
        </div>
      </div>
    </div>
  );
}