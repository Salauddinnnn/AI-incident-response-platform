import useDashboard from "../hooks/useDashboard";

export default function Infrastructure() {
  const { data, isLoading, isError } = useDashboard();

  const metrics = data?.metrics;

  if (isLoading) return <p>Loading...</p>;
  if (isError) return <p>Failed to load metrics.</p>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">
        Server Monitor
      </h1>

      <div className="grid md:grid-cols-3 gap-6">

        <div className="bg-white rounded-2xl shadow p-6">
          <h2 className="text-gray-500">CPU</h2>
          <p className="text-4xl font-bold mt-2">
            {metrics.cpu_percent}%
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow p-6">
          <h2 className="text-gray-500">RAM</h2>
          <p className="text-4xl font-bold mt-2">
            {metrics.ram_percent}%
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow p-6">
          <h2 className="text-gray-500">Disk</h2>
          <p className="text-4xl font-bold mt-2">
            {metrics.disk_percent}%
          </p>
        </div>

      </div>
    </div>
  );
}