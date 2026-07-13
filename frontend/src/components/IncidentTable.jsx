export default function IncidentTable({ incidents = [] }) {
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

  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="mb-5 text-xl font-bold">Recent Incidents</h2>

      {incidents.length === 0 ? (
        <p className="text-sm text-slate-500">No recent incidents.</p>
      ) : (
        <table className="w-full">
          <thead>
            <tr className="border-b text-left text-sm text-slate-500">
              <th className="py-3 pr-4">Title</th>
              <th className="py-3 pr-4">Website</th>
              <th className="py-3 pr-4">Severity</th>
              <th className="py-3 pr-4">Status</th>
              <th className="py-3">Date</th>
            </tr>
          </thead>

          <tbody>
            {incidents.map((item) => (
              <tr key={item.id} className="border-b text-sm">
                <td className="py-4 pr-4 font-medium text-slate-900">
                  {item.title}
                </td>
                <td className="py-4 pr-4 text-slate-500">
                  {item.website_name || "-"}
                </td>
                <td className="py-4 pr-4">
                  <span
                    className={`rounded-full px-2 py-0.5 text-xs font-medium ${severityBadge(item.severity)}`}
                  >
                    {item.severity}
                  </span>
                </td>
                <td className="py-4 pr-4">
                  <span
                    className={`rounded-full px-2 py-0.5 text-xs font-medium ${statusBadge(item.status)}`}
                  >
                    {item.status}
                  </span>
                </td>
                <td className="py-4 text-slate-500">
                  {item.created_at
                    ? new Date(item.created_at).toLocaleDateString()
                    : "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}