import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";

export default function SSLMonitor() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["ssl-check"],
    queryFn: async () => {
      const response = await api.get("/ssl-check");
      return response.data;
    },
    refetchInterval: 60000,
  });

  if (isLoading) {
    return <p className="text-slate-500">Loading SSL status...</p>;
  }

  if (isError) {
    return <p className="text-red-600">Failed to load SSL status.</p>;
  }

  const daysLeft = data?.ssl_days_left ?? 0;

  return (
    <div>
      <h1 className="mb-6 text-3xl font-bold text-slate-900">
        SSL Monitor
      </h1>

      <div className="rounded-2xl bg-white p-6 shadow-sm">
        <p className="text-sm text-slate-500">Hostname</p>
        <h2 className="mt-1 text-xl font-semibold">
          {data?.hostname}
        </h2>

        <div className="mt-6 grid gap-5 md:grid-cols-2">
          <div className="rounded-xl bg-slate-50 p-5">
            <p className="text-sm text-slate-500">Expiry Date</p>
            <p className="mt-2 text-2xl font-bold">
              {data?.ssl_expiry_date}
            </p>
          </div>

          <div className="rounded-xl bg-slate-50 p-5">
            <p className="text-sm text-slate-500">Days Left</p>
            <p
              className={`mt-2 text-2xl font-bold ${
                daysLeft <= 15
                  ? "text-red-600"
                  : daysLeft <= 30
                  ? "text-amber-600"
                  : "text-green-600"
              }`}
            >
              {daysLeft}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}