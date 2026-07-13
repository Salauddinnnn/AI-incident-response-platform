import useDashboard from "../hooks/useDashboard";

export default function Reports() {
  const { data, isLoading, isError } = useDashboard();

  if (isLoading) return <p>Loading reports...</p>;
  if (isError) return <p>Failed to load reports.</p>;

  const incidents = data?.incidents?.incidents || [];

  const critical = incidents.filter(i => i.severity === "critical").length;
  const warning = incidents.filter(i => i.severity === "warning").length;
  const resolved = incidents.filter(i => i.status === "resolved").length;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">
        Reports
      </h1>

      <div className="grid md:grid-cols-4 gap-6">

        <div className="bg-white rounded-2xl p-6 shadow">
          <h2 className="text-gray-500">Total Incidents</h2>
          <p className="text-4xl font-bold mt-2">
            {incidents.length}
          </p>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow">
          <h2 className="text-gray-500">Critical</h2>
          <p className="text-4xl font-bold text-red-600 mt-2">
            {critical}
          </p>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow">
          <h2 className="text-gray-500">Warning</h2>
          <p className="text-4xl font-bold text-yellow-500 mt-2">
            {warning}
          </p>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow">
          <h2 className="text-gray-500">Resolved</h2>
          <p className="text-4xl font-bold text-green-600 mt-2">
            {resolved}
          </p>
        </div>

      </div>
    </div>
  );
}