import { Navigate, Route, Routes } from "react-router-dom";
import AppShell from "../components/AppShell";
import ProtectedRoute from "../components/ProtectedRoute";
import ApprovalsPage from "../pages/ApprovalsPage";
import CreateRequestPage from "../pages/CreateRequestPage";
import DashboardPage from "../pages/DashboardPage";
import LoginPage from "../pages/LoginPage";

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<AppShell />}>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/requests/new" element={<CreateRequestPage />} />
          <Route path="/approvals" element={<ApprovalsPage />} />
        </Route>
      </Route>

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

export default AppRoutes;
