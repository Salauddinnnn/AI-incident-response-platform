import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import Dashboard from "../pages/Dashboard";

export default function DashboardLayout() {
  return (
    <div className="min-h-screen flex bg-slate-100">

      <Sidebar />

      <main className="flex-1 p-8">

        <Navbar />

        <Dashboard />

      </main>

    </div>
  );
}