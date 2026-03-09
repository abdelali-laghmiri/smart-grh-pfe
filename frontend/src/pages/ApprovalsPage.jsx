import { useEffect, useState } from "react";
import StatusBadge from "../components/StatusBadge";
import { api } from "../services/api";

function ApprovalsPage() {
  const [approvals, setApprovals] = useState([]);
  const [comments, setComments] = useState({});
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [activeRequestId, setActiveRequestId] = useState(null);

  async function loadApprovals() {
    setIsLoading(true);
    setError("");

    try {
      const approvalsData = await api.getApprovals();
      setApprovals(approvalsData);
    } catch (loadError) {
      setError(loadError.message || "Unable to load approvals.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadApprovals();
  }, []);

  async function handleAction(requestId, action) {
    setActiveRequestId(requestId);
    setError("");

    try {
      if (action === "approve") {
        await api.approveRequest(requestId, comments[requestId]);
      } else {
        await api.rejectRequest(requestId, comments[requestId]);
      }

      await loadApprovals();
    } catch (actionError) {
      setError(actionError.message || "Unable to process approval action.");
    } finally {
      setActiveRequestId(null);
    }
  }

  return (
    <section className="stack-page">
      <header className="panel">
        <p className="eyebrow">Workflow</p>
        <h2>Pending approvals</h2>
        <p className="muted">Approve or reject requests currently assigned to you.</p>
      </header>

      {error ? <div className="panel form-error">{error}</div> : null}

      <section className="panel">
        {isLoading ? (
          <p className="muted">Loading approvals...</p>
        ) : approvals.length ? (
          <div className="list-stack">
            {approvals.map((approval) => {
              const isBusy = activeRequestId === approval.request_id;

              return (
                <article key={approval.id} className="list-card approval-card">
                  <div className="list-card-header">
                    <div>
                      <h3>Request #{approval.request_id}</h3>
                      <p className="muted">Step {approval.step_order}</p>
                    </div>
                    <StatusBadge value={approval.status} />
                  </div>

                  <p className="muted">Approver user #{approval.approver_user_id}</p>

                  <label className="field-block" htmlFor={`comment-${approval.id}`}>
                    <span className="field-label">Comment</span>
                    <textarea
                      id={`comment-${approval.id}`}
                      rows="3"
                      className="input-control"
                      placeholder="Optional manager feedback"
                      value={comments[approval.request_id] || ""}
                      onChange={(event) =>
                        setComments((current) => ({
                          ...current,
                          [approval.request_id]: event.target.value
                        }))
                      }
                      disabled={isBusy}
                    />
                  </label>

                  <div className="action-row">
                    <button
                      className="primary-button"
                      type="button"
                      onClick={() => handleAction(approval.request_id, "approve")}
                      disabled={isBusy}
                    >
                      {isBusy ? "Processing..." : "Approve"}
                    </button>
                    <button
                      className="danger-button"
                      type="button"
                      onClick={() => handleAction(approval.request_id, "reject")}
                      disabled={isBusy}
                    >
                      Reject
                    </button>
                  </div>
                </article>
              );
            })}
          </div>
        ) : (
          <div className="empty-state">
            <p>No approvals are waiting right now.</p>
          </div>
        )}
      </section>
    </section>
  );
}

export default ApprovalsPage;
