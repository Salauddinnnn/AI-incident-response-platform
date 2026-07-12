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

import { NavLink } from "react-router-dom";

const menu = [
  {
    icon: LayoutDashboard,
    label: "Dashboard",
    path: "/",
  },
  {
    icon: Activity,
    label: "Incidents",
    path: "/incidents",
  },
  {
    icon: Globe,
    label: "Website Monitor",
    path: "/websites",
  },
  {
    icon: Server,
    label: "Infrastructure",
    path: "/infrastructure",
  },
  {
    icon: ShieldAlert,
    label: "AI Analysis",
    path: "/ai-analysis",
  },
  {
    icon: Lock,
    label: "SSL Monitor",
    path: "/ssl",
  },
  {
    icon: BarChart3,
    label: "Reports",
    path: "/reports",
  },
  {
    icon: Settings,
    label: "Settings",
    path: "/settings",
  },
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
            <NavLink
              key={item.label}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl transition ${
                  isActive
                    ? "bg-blue-600"
                    : "hover:bg-slate-800"
                }`
              }
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </div>
    </aside>
  );
}