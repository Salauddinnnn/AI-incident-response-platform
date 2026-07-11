export default function IncidentTable({ incidents = [] }) {
  return (
    <div className="bg-white rounded-2xl shadow-sm mt-8 p-6">
      <h2 className="text-xl font-bold mb-5">
        Recent Incidents
      </h2>

      <table className="w-full">
        <thead>
          <tr className="border-b">
            <th className="text-left py-3">Title</th>
            <th className="text-left py-3">Severity</th>
            <th className="text-left py-3">Status</th>
          </tr>
        </thead>

        <tbody>
          {incidents.map((item) => (
            <tr key={item.id} className="border-b">
              <td className="py-4">{item.title}</td>
              <td className="py-4">{item.severity}</td>
              <td className="py-4">{item.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}