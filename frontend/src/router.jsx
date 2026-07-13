import { createBrowserRouter } from "react-router-dom";
import AddWebsite from "./pages/AddWebsite";
import DashboardLayout from "./layouts/DashboardLayout";
import ProtectedRoute from "./components/ProtectedRoute";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Incidents from "./pages/Incidents";
import Websites from "./pages/Websites";
import Infrastructure from "./pages/Infrastructure";
import AIAnalysis from "./pages/AIAnalysis";
import SSLMonitor from "./pages/SSLMonitor";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";
import Login from "./pages/Login";

const router = createBrowserRouter([
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/register",
    element: <Register />,
  },
  {
    path: "/",
    element: (
      <ProtectedRoute>
        <DashboardLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: "incidents",
        element: <Incidents />,
      },
      {
        path: "websites",
        element: <Websites />,
      },
      {
        path: "infrastructure",
        element: <Infrastructure />,
      },
      {
        path: "ai-analysis",
        element: <AIAnalysis />,
      },
      {
        path: "ssl",
        element: <SSLMonitor />,
      },
      {
        path: "reports",
        element: <Reports />,
      },
      {
        path: "settings",
        element: <Settings />,
      },
      
      {
        path: "websites/add",
        element: <AddWebsite />,
     },
    ],
  },
]);

export default router;