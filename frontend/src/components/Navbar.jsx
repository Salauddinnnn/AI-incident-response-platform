import { Bell, Search, UserCircle } from "lucide-react";

export default function Navbar() {
  return (
    <div className="flex justify-between items-center bg-white rounded-2xl shadow-sm p-5 mb-8">
      <div>
        <h2 className="text-2xl font-bold">Dashboard</h2>
        <p className="text-gray-500">
          AI Incident Response Platform
        </p>
      </div>

      <div className="flex items-center gap-5">
        <Search size={22} className="text-gray-500" />
        <Bell size={22} className="text-gray-500" />
        <UserCircle size={36} className="text-blue-600" />
      </div>
    </div>
  );
}