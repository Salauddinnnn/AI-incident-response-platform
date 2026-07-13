import { useMemo, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../services/api";

export default function Incidents() {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [severity, setSeverity] = useState("all");
  const [status, setStatus] = useState("all");
  const [selectedIncident, setSelectedIncident] = useState(null);

  const { data, isLoading, isError } = useQuery({
    queryKey: ["incidents", search, severity, status],
    queryFn: async () => {
      const params = {};
      if (search) params.search = search;
      if (severity !== "all") params.severity = severity;
      if (status !== "all") params.status = status;

      const response = await api.get("/incidents", { params });
      return response.data;
    },
  });

  const incidents = data?.incidents || [];

  async function handleResolve(incidentId) {
    try {
      await api.patch(`/incidents/${incidentId}/resolve`);
      queryClient.invalidateQueries({ queryKey: ["incidents"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    } catch (error) {
      console.error("Failed to resolve incident:", error);
    }
  }

  const severityBadge = (sev) => {
    switch (sev) {
      case "critical":
        return "bg-red-100 text-red-700";
      case "warning":
        return "bg-yellow-100 text-yellow-700";
      default:
        return "bg-green-100 text-green-700";
    }
  };

  const statusBadge = (st) => {
    switch (st) {
      case "open":
        return "bg-blue-100 text-blue-700";
      case "resolved":
        return "bg-slate-100 text-slate-600";
      default:
        return "bg-slate-100 text-slate-600";
    }
  };

  if (isLoading) {
    return <p className="text-slate-500">Loading incidents...</p>;
  }

  if (isError) {
    return <p className="text-red-600">Failed to load incidents.</p>;
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-900">Incidents</h1>
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

        <select
          value={status}
          onChange={(event) => setStatus(event.target.value)}
          className="rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-blue-500"
        >
          <option value="all">All status</option>
          <option value="open">Open</option>
          <option value="resolved">Resolved</option>
        </select>
      </div>

      <div className="space-y-4">
        {incidents.map((incident) => (
          <div
            key={incident.id}
            className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
          >
            <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
              <div className="min-w-0 flex-1">
                <h2 className="text-lg font-semibold text-slate-900">
                  {incident.title}
                </h2>
                <p className="mt-1 text-sm text-slate-500">
                  {incident.website_name && (
                    <span className="font-medium">{incident.website_name}</span>
                  )}
                  {incident.website_url && (
                    <span className="ml-1 text-slate-400">
                      ({incident.website_url})
                    </span>
                  )}
                </p>
                <p className="mt-1 text-sm text-slate-500">
                  {incident.created_at
                    ? new Date(incident.created_at).toLocaleString()
                    : "No date"}
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <span
                  className={`rounded-full px-3 py-1 text-sm font-medium ${severityBadge(incident.severity)}`}
                >
                  {incident.severity}
                </span>

                <span
                  className={`rounded-full px-3 py-1 text-sm font-medium ${statusBadge(incident.status)}`}
                >
                  {incident.status}
                </span>

                <button
                  onClick={() => setSelectedIncident(incident)}
                  className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
                >
                  View Details
                </button>

                {incident.status === "open" && (
                  <button
                    onClick={() => handleResolve(incident.id)}
                    className="rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700"
                  >
                    Resolve
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}

        {incidents.length === 0 && (
          <div className="rounded-2xl bg-white p-8 text-center text-slate-500 shadow-sm">
            No incidents found.
          </div>
        )}
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
                {selectedIncident.website_name && (
                  <p className="mt-1 text-sm text-slate-500">
                    Website: {selectedIncident.website_name}
                    {selectedIncident.website_url && (
                      <span className="ml-1 text-slate-400">
                        ({selectedIncident.website_url})
                      </span>
                    )}
                  </p>
                )}
              </div>

              <button
                onClick={() => setSelectedIncident(null)}
                className="text-2xl text-slate-500 hover:text-slate-700"
              >
                ×
              </button>
            </div>

            <div className="mt-6">
              <h3 className="mb-2 text-lg font-semibold text-slate-800">
                AI Analysis
              </h3>
              <div className="whitespace-pre-wrap rounded-xl bg-slate-50 p-5 text-sm leading-7 text-slate-700">
                {selectedIncident.ai_summary || "No AI analysis available."}
              </div>
            </div>

            {selectedIncident.auto_heal_report && (
              <div className="mt-4">
                <h3 className="mb-2 text-lg font-semibold text-slate-800">
                  Auto-Healing Report
                </h3>
                <div className="whitespace-pre-wrap rounded-xl bg-blue-50 p-5 text-sm leading-7 text-slate-700">
                  {selectedIncident.auto_heal_report}
                </div>
              </div>
            )}

            {selectedIncident.status === "open" && (
              <button
                onClick={() => {
                  handleResolve(selectedIncident.id);
                  setSelectedIncident(null);
                }}
                className="mt-4 rounded-lg bg-green-600 px-5 py-3 font-medium text-white hover:bg-green-700"
              >
                Resolve Incident
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}