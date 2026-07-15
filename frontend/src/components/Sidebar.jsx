import {
  LayoutDashboard,
  Activity,
  ShieldAlert,
  Server,
  Globe,
  Lock,
  Settings,
  BarChart3,
  X,
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

export default function Sidebar({ isOpen, onClose }) {
  return (
    <>
      {/* Desktop sidebar - always visible */}
      <aside className="hidden h-screen w-64 shrink-0 bg-slate-900 p-6 text-white lg:block">
        <h1 className="mb-10 text-2xl font-bold">AI Incident</h1>

        <nav className="space-y-2">
          {menu.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.label}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-xl px-4 py-3 transition ${
                    isActive ? "bg-blue-600" : "hover:bg-slate-800"
                  }`
                }
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </aside>

      {/* Mobile sidebar overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Mobile sidebar drawer */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-64 -translate-x-full transform overflow-y-auto bg-slate-900 p-6 text-white transition-transform duration-200 ease-in-out lg:hidden ${
          isOpen ? "translate-x-0" : ""
        }`}
      >
        <div className="mb-10 flex items-center justify-between">
          <h1 className="text-2xl font-bold">AI Incident</h1>
          <button
            onClick={onClose}
            className="rounded-lg p-1 text-white hover:bg-slate-800"
            aria-label="Close menu"
          >
            <X size={24} />
          </button>
        </div>

        <nav className="space-y-2">
          {menu.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.label}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-xl px-4 py-3 transition ${
                    isActive ? "bg-blue-600" : "hover:bg-slate-800"
                  }`
                }
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </aside>
    </>
  );
}