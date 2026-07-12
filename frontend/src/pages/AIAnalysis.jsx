import useDashboard from "../hooks/useDashboard";

export default function AIAnalysis() {
  const { data, isLoading, isError } = useDashboard();

  const incidents = data?.incidents?.incidents || [];

  if (isLoading) {
    return <p className="text-slate-500">Loading AI analysis...</p>;
  }

  if (isError) {
    return <p className="text-red-600">Failed to load AI analysis.</p>;
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-900">
          AI Analysis
        </h1>

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
                  {incident.created_at
                    ? new Date(incident.created_at).toLocaleString()
                    : "No date"}
                </p>
              </div>

              <span className="h-fit rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">
                {incident.severity}
              </span>
            </div>

            <div className="mt-5 whitespace-pre-line rounded-xl bg-slate-50 p-5 text-sm leading-7 text-slate-700">
              {incident.ai_summary || "No AI analysis available."}
            </div>
          </div>
        ))}

        {incidents.length === 0 && (
          <div className="rounded-2xl bg-white p-8 text-center text-slate-500 shadow-sm">
            No AI analysis found.
          </div>
        )}
      </div>
    </div>
  );
}