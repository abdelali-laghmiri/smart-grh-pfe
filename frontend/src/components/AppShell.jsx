import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const navigation = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/requests/new", label: "Create Request" },
  { to: "/approvals", label: "Approvals" }
];

function AppShell() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-card">
          <p className="eyebrow">Smart GRH</p>
          <h1>HR Requests</h1>
          <p className="muted">A focused workspace for employee requests and approvals.</p>
        </div>

        <nav className="nav-list" aria-label="Main navigation">
          {navigation.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                isActive ? "nav-link nav-link-active" : "nav-link"
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="user-card">
          <p className="user-name">{user?.matricule}</p>
          <p className="muted">{user?.role || "Employee"}</p>
          <button className="secondary-button" type="button" onClick={handleLogout}>
            Log Out
          </button>
        </div>
      </aside>

      <main className="content-shell">
        <Outlet />
      </main>
    </div>
  );
}

export default AppShell;
