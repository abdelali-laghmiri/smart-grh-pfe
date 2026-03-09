import { useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

function LoginPage() {
  const { isAuthenticated, isInitializing, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [formState, setFormState] = useState({
    matricule: "",
    password: ""
  });
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (isInitializing) {
    return (
      <div className="page-shell centered-shell">
        <div className="panel">
          <p className="eyebrow">Loading session</p>
          <h1>Checking saved credentials</h1>
        </div>
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      await login(formState);
      const nextPath = location.state?.from?.pathname || "/dashboard";
      navigate(nextPath, { replace: true });
    } catch (submissionError) {
      setError(submissionError.message || "Unable to sign in.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="page-shell auth-shell">
      <section className="auth-hero">
        <p className="eyebrow">Progressive Web App</p>
        <h1>Smart GRH frontend</h1>
        <p className="hero-copy">
          Sign in to track your requests, submit new ones, and review approvals from a single lightweight workspace.
        </p>
      </section>

      <section className="panel auth-panel">
        <div>
          <p className="eyebrow">Authentication</p>
          <h2>Login</h2>
        </div>

        <form className="stack-form" onSubmit={handleSubmit}>
          <label className="field-block" htmlFor="matricule">
            <span className="field-label">Matricule</span>
            <input
              id="matricule"
              name="matricule"
              type="text"
              className="input-control"
              value={formState.matricule}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  matricule: event.target.value
                }))
              }
              required
            />
          </label>

          <label className="field-block" htmlFor="password">
            <span className="field-label">Password</span>
            <input
              id="password"
              name="password"
              type="password"
              className="input-control"
              value={formState.password}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  password: event.target.value
                }))
              }
              required
            />
          </label>

          {error ? <p className="form-error">{error}</p> : null}

          <button className="primary-button" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Signing in..." : "Sign In"}
          </button>
        </form>
      </section>
    </div>
  );
}

export default LoginPage;
