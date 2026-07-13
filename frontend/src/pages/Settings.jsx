export default function Settings() {
  return (
    <div>
      <h1 className="mb-6 text-3xl font-bold text-slate-900">
        Settings
      </h1>

      <div className="space-y-5">
        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold">
            Monitoring Settings
          </h2>

          <div className="mt-5 grid gap-4 md:grid-cols-2">
            <div>
              <label className="text-sm text-slate-500">
                Slow Threshold
              </label>

              <input
                value="2.0 seconds"
                readOnly
                className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3"
              />
            </div>

            <div>
              <label className="text-sm text-slate-500">
                Request Timeout
              </label>

              <input
                value="10 seconds"
                readOnly
                className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3"
              />
            </div>
          </div>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold">
            Integrations
          </h2>

          <div className="mt-5 space-y-3 text-sm">
            <p>Gemini AI: Connected</p>
            <p>Email Alerts: Enabled</p>
            <p>Prometheus: Connected</p>
            <p>Grafana: Connected</p>
          </div>
        </div>
      </div>
    </div>
  );
}