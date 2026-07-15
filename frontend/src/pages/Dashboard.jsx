import {
  Activity,
  Globe,
  Server,
  Sparkles,
  AlertTriangle,
  CheckCircle,
  XCircle,
} from "lucide-react";
import IncidentTable from "../components/IncidentTable";
import StatCard from "../components/StatCard";
import { useEffect, useState } from "react";
import AIAnalysisCard from "../components/AIAnalysisCard";
import WebsiteStatus from "../components/WebsiteStatus";
import PerformanceChart from "../components/PerformanceChart";
import useDashboard from "../hooks/useDashboard";

export default function Dashboard() {
  const { data, isLoading, isError } = useDashboard();
  const [performanceData, setPerformanceData] = useState([]);

  useEffect(() => {
    if (!data?.metrics) return;

    const point = {
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }),
      cpu: Math.round(data.metrics.cpu_percent || 0),
      ram: Math.round(data.metrics.ram_percent || 0),
      disk: Math.round(data.metrics.disk_percent || 0),
    };

    setPerformanceData((current) => [...current.slice(-19), point]);
  }, [data?.metrics]);

  if (isLoading) {
    return <p className="text-slate-500">Loading dashboard...</p>;
  }

  if (isError) {
    return <p className="text-red-600">Backend connection failed.</p>;
  }

  const stats = data?.stats || {};
  const recentIncidents = data?.recent_incidents || [];
  const allIncidents = data?.recent_incidents || [];
  const websites = data?.websites || [];

  return (
    <div>
      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Total Websites"
          value={stats.total_websites || 0}
          subtitle={`${stats.healthy || 0} healthy • ${stats.slow || 0} slow • ${stats.down || 0} down`}
          icon={Globe}
        />

        <StatCard
          title="Open Incidents"
          value={stats.open_incidents || 0}
          subtitle={`${stats.critical_incidents || 0} critical • ${stats.total_incidents || 0} total`}
          icon={AlertTriangle}
        />

        <StatCard
          title="Server Health"
          value={`${Math.round(data?.metrics?.cpu_percent || 0)}% CPU`}
          subtitle={`RAM ${Math.round(data?.metrics?.ram_percent || 0)}% • Disk ${Math.round(data?.metrics?.disk_percent || 0)}%`}
          icon={Server}
        />

        <StatCard
          title="Avg Response Time"
          value={stats.avg_response_time ? `${stats.avg_response_time}s` : "N/A"}
          subtitle="Across all websites"
          icon={Activity}
        />
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <PerformanceChart data={performanceData} />
        </div>
        <div>
          <WebsiteStatus websites={websites} />
        </div>
      </div>

      <div className="mt-6">
        <IncidentTable incidents={recentIncidents} />
      </div>

      <div className="mt-6">
        <AIAnalysisCard incidents={recentIncidents} />
      </div>
    </div>
  );
}