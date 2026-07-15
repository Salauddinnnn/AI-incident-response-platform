import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";

export default function Reports() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["report-stats"],
    queryFn: async () => {
      const response = await api.get("/incidents");
      return response.data;
    },
  });

  if (isLoading) return <p className="text-slate-500">Loading reports...</p>;
  if (isError) return <p className="text-red-600">Failed to load reports.</p>;

  const incidents = data?.incidents || [];
  const stats = data?.stats || {};

  const critical = incidents.filter((i) => i.severity === "critical").length;
  const warning = incidents.filter((i) => i.severity === "warning").length;
  const resolved = incidents.filter((i) => i.status === "resolved").length;

  return (
    <div>
      <h1 className="mb-6 text-3xl font-bold text-slate-900">Reports</h1>
      <p className="mb-6 text-slate-500">
        Summary of all incidents across your monitored websites
      </p>

      <div className="grid gap-6 md:grid-cols-4">
        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="text-sm text-slate-500">Total Incidents</h2>
          <p className="mt-2 text-4xl font-bold text-slate-900">
            {stats.total || incidents.length}
          </p>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="text-sm text-slate-500">Open</h2>
          <p className="mt-2 text-4xl font-bold text-blue-600">
            {stats.open || incidents.filter((i) => i.status === "open").length}
          </p>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="text-sm text-slate-500">Critical</h2>
          <p className="mt-2 text-4xl font-bold text-red-600">{critical}</p>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="text-sm text-slate-500">Warning</h2>
          <p className="mt-2 text-4xl font-bold text-yellow-500">{warning}</p>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="text-sm text-slate-500">Resolved</h2>
          <p className="mt-2 text-4xl font-bold text-green-600">{resolved}</p>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="text-sm text-slate-500">Total Websites</h2>
          <p className="mt-2 text-4xl font-bold text-slate-900">
            {data?.stats?.total_websites || "-"}
          </p>
        </div>
      </div>

      {incidents.length > 0 && (
        <div className="mt-8">
          <h2 className="mb-4 text-xl font-bold text-slate-900">
            Recent Incidents
          </h2>
          <div className="space-y-3">
            {incidents.slice(0, 10).map((incident) => (
              <div
                key={incident.id}
                className="flex items-center justify-between rounded-xl border border-slate-100 bg-white p-4"
              >
                <div className="min-w-0 flex-1">
                  <p className="truncate font-medium text-slate-900">
                    {incident.title}
                  </p>
                  <p className="text-xs text-slate-500">
                    {incident.website_name || "Unknown website"}
                    {incident.created_at &&
                      ` · ${new Date(incident.created_at).toLocaleDateString()}`}
                  </p>
                </div>
                <div className="ml-3 flex items-center gap-2">
                  <span
                    className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                      incident.severity === "critical"
                        ? "bg-red-100 text-red-700"
                        : incident.severity === "warning"
                          ? "bg-yellow-100 text-yellow-700"
                          : "bg-green-100 text-green-700"
                    }`}
                  >
                    {incident.severity}
                  </span>
                  <span
                    className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                      incident.status === "open"
                        ? "bg-blue-100 text-blue-700"
                        : "bg-slate-100 text-slate-600"
                    }`}
                  >
                    {incident.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}