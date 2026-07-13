import { CheckCircle, AlertTriangle, XCircle, Minus } from "lucide-react";

export default function WebsiteStatus({ websites = [] }) {
  if (websites.length === 0) {
    return (
      <div className="rounded-2xl bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-bold">Website Status</h2>
        <p className="text-sm text-slate-500">No websites added yet.</p>
      </div>
    );
  }

  const statusIcon = (status) => {
    switch (status) {
      case "up":
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case "slow":
        return <AlertTriangle className="h-5 w-5 text-yellow-500" />;
      case "down":
        return <XCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Minus className="h-5 w-5 text-slate-400" />;
    }
  };

  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-xl font-bold">Website Status</h2>

      <div className="space-y-3">
        {websites.map((website) => (
          <div
            key={website.id}
            className="flex items-center justify-between rounded-xl border border-slate-100 p-3"
          >
            <div className="min-w-0 flex-1">
              <p className="truncate font-medium text-slate-900">
                {website.name}
              </p>
              <p className="truncate text-xs text-slate-500">
                {website.url}
              </p>
            </div>
            <div className="ml-3 flex items-center gap-2">
              {website.response_time_seconds && (
                <span className="text-xs text-slate-500">
                  {website.response_time_seconds}s
                </span>
              )}
              {statusIcon(website.current_status)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}