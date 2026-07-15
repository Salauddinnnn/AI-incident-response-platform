import { UserCircle, Menu, X } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Navbar({ onToggleSidebar, sidebarOpen }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="mb-8 flex items-center justify-between rounded-2xl bg-white p-5 shadow-sm">
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 lg:hidden"
          aria-label="Toggle menu"
        >
          {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
        </button>

        <div>
          <h2 className="text-2xl font-bold">Dashboard</h2>
          <p className="text-gray-500">AI Incident Response Platform</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="hidden text-right md:block">
          <p className="text-sm font-semibold">{user?.name || "Admin"}</p>
          <p className="text-xs text-gray-500">{user?.email || "admin@example.com"}</p>
        </div>

        <UserCircle size={38} className="text-blue-600" />

        <button
          onClick={handleLogout}
          className="rounded-xl bg-red-500 px-4 py-2 text-white transition hover:bg-red-600"
        >
          Logout
        </button>
      </div>
    </div>
  );
}