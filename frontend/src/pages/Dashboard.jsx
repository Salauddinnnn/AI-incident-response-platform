import {
  Activity,
  Globe,
  Server,
  Sparkles,
} from "lucide-react";
import IncidentTable from "../components/IncidentTable";
import StatCard from "../components/StatCard";
import useDashboard from "../hooks/useDashboard";

export default function Dashboard() {
  const { data, isLoading, isError } = useDashboard();

  if (isLoading) {
    return <p className="text-slate-500">Loading dashboard...</p>;
  }

  if (isError) {
    return <p className="text-red-600">Backend connection failed.</p>;
  }

  const incidents = data?.incidents?.incidents || [];
  const openIncidents = incidents.filter(
    (item) => item.status === "open"
  ).length;

  const websiteStatus =
    data?.health?.status?.toUpperCase() || "UNKNOWN";

  return (
    <div>
      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Active Incidents"
          value={openIncidents}
          subtitle={`${incidents.length} total incidents`}
          icon={Activity}
        />

        <StatCard
          title="Website Status"
          value={websiteStatus}
          subtitle="Live health check"
          icon={Globe}
        />

        <StatCard
        title="Server Health"
        value={`${Math.round(data?.metrics?.cpu_percent || 0)}% CPU`}
        subtitle={`RAM ${Math.round(data?.metrics?.ram_percent || 0)}% • Disk ${Math.round(data?.metrics?.disk_percent || 0)}%`}
        icon={Server}
      />

        <StatCard
          title="AI Analysis"
          value="Ready"
          subtitle="Gemini AI connected"
          icon={Sparkles}
        />
      </div>
      <IncidentTable incidents={incidents.slice(0, 5)} />
    </div>
  );
}