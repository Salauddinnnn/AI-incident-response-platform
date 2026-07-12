import { createBrowserRouter } from "react-router-dom";
import Websites from "./pages/Websites";
import Infrastructure from "./pages/Infrastructure";
import DashboardLayout from "./layouts/DashboardLayout";
import Dashboard from "./pages/Dashboard";
import Incidents from "./pages/Incidents";

const router = createBrowserRouter([
  {
    path: "/",
    element: <DashboardLayout />,
    children: [
        {
  path: "infrastructure",
  element: <Infrastructure />,
},
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

    ],
  },
]);

export default router;