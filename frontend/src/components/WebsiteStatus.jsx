export default function WebsiteStatus({ health }) {
  return (
    <div className="mt-8 rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="mb-5 text-xl font-bold">
        Website Status
      </h2>

      <div className="flex items-center justify-between">

        <div>
          <p className="text-gray-500">Current Status</p>

          <h1 className="mt-2 text-4xl font-bold">
            {health?.status?.toUpperCase()}
          </h1>
        </div>

        <div
          className={`h-5 w-5 rounded-full ${
            health?.status === "up"
              ? "bg-green-500"
              : health?.status === "slow"
              ? "bg-yellow-500"
              : "bg-red-500"
          }`}
        />
      </div>

      <p className="mt-6 text-gray-500">
        Response Time : {health?.response_time_seconds} sec
      </p>
    </div>
  );
}