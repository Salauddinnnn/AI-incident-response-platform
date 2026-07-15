import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";

export default function AIAnalysis() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["ai-analysis"],
    queryFn: async () => {
      const response = await api.get("/incidents", {
        params: { limit: 50 },
      });
      return response.data;
    },
  });

  const incidents = data?.incidents || [];

  if (isLoading) {
    return <p className="text-slate-500">Loading AI analysis...</p>;
  }

  if (isError) {
    return <p className="text-red-600">Failed to load AI analysis.</p>;
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-900">AI Analysis</h1>
        <p className="mt-1 text-slate-500">
          Gemini-powered incident analysis and recommendations
        </p>
      </div>

      <div className="space-y-5">
        {incidents.map((incident) => (
          <div
            key={incident.id}
            className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
          >
            <div className="flex flex-col justify-between gap-3 md:flex-row">
              <div>
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

              <div className="flex items-center gap-2">
                <span
                  className={`h-fit rounded-full px-3 py-1 text-sm font-medium ${
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
                  className={`h-fit rounded-full px-3 py-1 text-sm font-medium ${
                    incident.status === "open"
                      ? "bg-blue-100 text-blue-700"
                      : "bg-slate-100 text-slate-600"
                  }`}
                >
                  {incident.status}
                </span>
              </div>
            </div>

            <div className="mt-5 whitespace-pre-line rounded-xl bg-slate-50 p-5 text-sm leading-7 text-slate-700">
              {incident.ai_summary || "No AI analysis available."}
            </div>

            {incident.auto_heal_report && (
              <div className="mt-4 rounded-xl bg-blue-50 p-4 text-sm leading-6 text-slate-700">
                <h3 className="mb-2 font-semibold text-slate-800">
                  Auto-Healing Report
                </h3>
                <div className="whitespace-pre-line">
                  {incident.auto_heal_report}
                </div>
              </div>
            )}
          </div>
        ))}

        {incidents.length === 0 && (
          <div className="rounded-2xl bg-white p-8 text-center text-slate-500 shadow-sm">
            No AI analysis found. Incidents will appear here after they are
            detected and analyzed.
          </div>
        )}
      </div>
    </div>
  );
}