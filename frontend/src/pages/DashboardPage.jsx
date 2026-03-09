import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import StatusBadge from "../components/StatusBadge";
import { useAuth } from "../hooks/useAuth";
import { api } from "../services/api";

function formatDate(value) {
  if (!value) {
    return "Unknown date";
  }

  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(value));
}

function DashboardPage() {
  const { user } = useAuth();
  const [myRequests, setMyRequests] = useState([]);
  const [approvals, setApprovals] = useState([]);
  const [requestTypes, setRequestTypes] = useState([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      setIsLoading(true);
      setError("");

      try {
        const [requestsData, approvalsData, typesData] = await Promise.all([
          api.getMyRequests(),
          api.getApprovals(),
          api.getRequestTypes()
        ]);

        setMyRequests(requestsData);
        setApprovals(approvalsData);
        setRequestTypes(typesData);
      } catch (loadError) {
        setError(loadError.message || "Unable to load dashboard data.");
      } finally {
        setIsLoading(false);
      }
    }

    loadDashboard();
  }, []);

  function getRequestTypeName(requestTypeId) {
    return requestTypes.find((item) => item.id === requestTypeId)?.name || `Type #${requestTypeId}`;
  }

  return (
    <section className="stack-page">
      <header className="panel hero-panel">
        <div>
          <p className="eyebrow">Dashboard</p>
          <h2>Welcome back, {user?.matricule}</h2>
          <p className="muted">
            Review your submitted requests and check whether approvals are waiting for action.
          </p>
        </div>
        <div className="metric-strip">
          <div className="metric-card">
            <span className="metric-value">{myRequests.length}</span>
            <span className="metric-label">My Requests</span>
          </div>
          <div className="metric-card">
            <span className="metric-value">{approvals.length}</span>
            <span className="metric-label">Pending Approvals</span>
          </div>
        </div>
      </header>

      {error ? <div className="panel form-error">{error}</div> : null}

      <div className="content-grid">
        <section className="panel">
          <div className="section-header">
            <div>
              <p className="eyebrow">Requests</p>
              <h3>My Requests</h3>
            </div>
            <Link className="secondary-button inline-link" to="/requests/new">
              New Request
            </Link>
          </div>

          {isLoading ? (
            <p className="muted">Loading requests...</p>
          ) : myRequests.length ? (
            <div className="list-stack">
              {myRequests.map((request) => (
                <article key={request.id} className="list-card">
                  <div className="list-card-header">
                    <div>
                      <h4>{getRequestTypeName(request.request_type_id)}</h4>
                      <p className="muted">Request #{request.id}</p>
                    </div>
                    <StatusBadge value={request.status} />
                  </div>
                  <p className="muted">Created {formatDate(request.created_at)}</p>
                  <p className="muted">Current step: {request.current_step ?? "Completed"}</p>
                </article>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No requests submitted yet.</p>
            </div>
          )}
        </section>

        <section className="panel">
          <div className="section-header">
            <div>
              <p className="eyebrow">Approvals</p>
              <h3>Requests To Approve</h3>
            </div>
            <Link className="secondary-button inline-link" to="/approvals">
              Open Approvals
            </Link>
          </div>

          {isLoading ? (
            <p className="muted">Loading approvals...</p>
          ) : approvals.length ? (
            <div className="list-stack">
              {approvals.map((approval) => (
                <article key={approval.id} className="list-card">
                  <div className="list-card-header">
                    <div>
                      <h4>Request #{approval.request_id}</h4>
                      <p className="muted">Step {approval.step_order}</p>
                    </div>
                    <StatusBadge value={approval.status} />
                  </div>
                  <p className="muted">
                    Approval assigned to user #{approval.approver_user_id}
                  </p>
                </article>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No pending approvals for your account.</p>
            </div>
          )}
        </section>
      </div>
    </section>
  );
}

export default DashboardPage;
