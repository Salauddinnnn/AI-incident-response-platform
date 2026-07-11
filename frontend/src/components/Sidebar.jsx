import {
  LayoutDashboard,
  Activity,
  ShieldAlert,
  Server,
  Globe,
  Lock,
  Settings,
  BarChart3,
} from "lucide-react";

const menu = [
  { icon: LayoutDashboard, label: "Dashboard" },
  { icon: Activity, label: "Incidents" },
  { icon: Globe, label: "Website Monitor" },
  { icon: Server, label: "Server Monitor" },
  { icon: ShieldAlert, label: "AI Analysis" },
  { icon: Lock, label: "SSL Monitor" },
  { icon: BarChart3, label: "Reports" },
  { icon: Settings, label: "Settings" },
];

export default function Sidebar() {
  return (
    <aside className="w-64 h-screen bg-slate-900 text-white p-6">
      <h1 className="text-2xl font-bold mb-10">
        AI Incident
      </h1>

      <div className="space-y-2">
        {menu.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              className="flex items-center gap-3 w-full px-4 py-3 rounded-xl hover:bg-slate-800 transition"
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>
    </aside>
  );
}