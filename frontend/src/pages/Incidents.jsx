import { useMemo, useState } from "react";
import useDashboard from "../hooks/useDashboard";

export default function Incidents() {
  const { data, isLoading, isError } = useDashboard();

  const [search, setSearch] = useState("");
  const [severity, setSeverity] = useState("all");
  const [selectedIncident, setSelectedIncident] = useState(null);

  const incidents = data?.incidents?.incidents || [];

  const filteredIncidents = useMemo(() => {
    return incidents.filter((incident) => {
      const matchesSearch = incident.title
        .toLowerCase()
        .includes(search.toLowerCase());

      const matchesSeverity =
        severity === "all" || incident.severity === severity;

      return matchesSearch && matchesSeverity;
    });
  }, [incidents, search, severity]);

  if (isLoading) {
    return <p className="text-slate-500">Loading incidents...</p>;
  }

  if (isError) {
    return <p className="text-red-600">Failed to load incidents.</p>;
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-900">
          Incidents
        </h1>

        <p className="mt-1 text-slate-500">
          Monitor and review detected incidents
        </p>
      </div>

      <div className="mb-6 flex flex-col gap-4 rounded-2xl bg-white p-5 shadow-sm md:flex-row">
        <input
          type="text"
          placeholder="Search incidents..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          className="flex-1 rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-blue-500"
        />

        <select
          value={severity}
          onChange={(event) => setSeverity(event.target.value)}
          className="rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-blue-500"
        >
          <option value="all">All severity</option>
          <option value="critical">Critical</option>
          <option value="warning">Warning</option>
          <option value="normal">Normal</option>
        </select>
      </div>

      <div className="space-y-4">
        {filteredIncidents.map((incident) => (
          <div
            key={incident.id}
            className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
          >
            <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
              <div>
                <h2 className="text-lg font-semibold text-slate-900">
                  {incident.title}
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  {incident.created_at
                    ? new Date(incident.created_at).toLocaleString()
                    : "No date"}
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <span className="rounded-full bg-red-100 px-3 py-1 text-sm font-medium text-red-700">
                  {incident.severity}
                </span>

                <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">
                  {incident.status}
                </span>

                <button
                  onClick={() => setSelectedIncident(incident)}
                  className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
                >
                  View Details
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {selectedIncident && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="max-h-[85vh] w-full max-w-3xl overflow-y-auto rounded-2xl bg-white p-6 shadow-xl">
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-2xl font-bold">
                  {selectedIncident.title}
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  {selectedIncident.severity} · {selectedIncident.status}
                </p>
              </div>

              <button
                onClick={() => setSelectedIncident(null)}
                className="text-2xl text-slate-500"
              >
                ×
              </button>
            </div>

            <div className="mt-6 whitespace-pre-wrap rounded-xl bg-slate-50 p-5 text-sm leading-7 text-slate-700">
              {selectedIncident.ai_summary || "No AI analysis available."}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}