import { createBrowserRouter } from "react-router-dom";

import DashboardLayout from "./layouts/DashboardLayout";

const router = createBrowserRouter([
  {
    path: "/",
    element: <DashboardLayout />,
  },
]);

export default router;