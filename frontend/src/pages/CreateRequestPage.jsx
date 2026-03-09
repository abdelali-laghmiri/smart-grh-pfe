import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import DynamicForm from "../components/DynamicForm";
import { api } from "../services/api";

function getInitialValues(fields) {
  return fields.reduce((accumulator, field) => {
    if (field.default_value !== null && field.default_value !== undefined) {
      accumulator[field.name] = field.default_value;
      return accumulator;
    }

    accumulator[field.name] = field.field_type === "BOOLEAN" ? false : "";
    return accumulator;
  }, {});
}

function compactExtraData(values) {
  return Object.entries(values).reduce((accumulator, [key, value]) => {
    if (value === "" || value === null || value === undefined) {
      return accumulator;
    }

    accumulator[key] = value;
    return accumulator;
  }, {});
}

function CreateRequestPage() {
  const navigate = useNavigate();
  const [requestTypes, setRequestTypes] = useState([]);
  const [selectedTypeId, setSelectedTypeId] = useState("");
  const [formSchema, setFormSchema] = useState(null);
  const [formValues, setFormValues] = useState({});
  const [error, setError] = useState("");
  const [isLoadingTypes, setIsLoadingTypes] = useState(true);
  const [isLoadingForm, setIsLoadingForm] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    async function loadTypes() {
      setIsLoadingTypes(true);
      setError("");

      try {
        const types = await api.getRequestTypes();
        setRequestTypes(types);
      } catch (loadError) {
        setError(loadError.message || "Unable to load request types.");
      } finally {
        setIsLoadingTypes(false);
      }
    }

    loadTypes();
  }, []);

  useEffect(() => {
    async function loadForm() {
      if (!selectedTypeId) {
        setFormSchema(null);
        setFormValues({});
        return;
      }

      setIsLoadingForm(true);
      setError("");

      try {
        const schema = await api.getRequestForm(selectedTypeId);
        setFormSchema(schema);
        setFormValues(getInitialValues(schema.fields));
      } catch (loadError) {
        setError(loadError.message || "Unable to load the form schema.");
      } finally {
        setIsLoadingForm(false);
      }
    }

    loadForm();
  }, [selectedTypeId]);

  function handleFieldChange(name, value) {
    setFormValues((current) => ({
      ...current,
      [name]: value
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      await api.createRequest({
        request_type_id: Number(selectedTypeId),
        extra_data: compactExtraData(formValues)
      });
      navigate("/dashboard", { replace: true });
    } catch (submissionError) {
      setError(submissionError.message || "Unable to submit the request.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section className="stack-page">
      <header className="panel">
        <p className="eyebrow">Request Builder</p>
        <h2>Create a new request</h2>
        <p className="muted">
          Choose a request type and the form will be generated from the backend configuration.
        </p>
      </header>

      <form className="panel stack-form" onSubmit={handleSubmit}>
        <label className="field-block" htmlFor="request-type">
          <span className="field-label">Request Type</span>
          <select
            id="request-type"
            className="input-control"
            value={selectedTypeId}
            onChange={(event) => setSelectedTypeId(event.target.value)}
            disabled={isLoadingTypes || isSubmitting}
            required
          >
            <option value="">Select a request type</option>
            {requestTypes.map((type) => (
              <option key={type.id} value={type.id}>
                {type.name}
              </option>
            ))}
          </select>
        </label>

        {error ? <p className="form-error">{error}</p> : null}

        {isLoadingTypes ? <p className="muted">Loading request types...</p> : null}
        {isLoadingForm ? <p className="muted">Loading dynamic form...</p> : null}

        {formSchema ? (
          <>
            <div className="subsection-header">
              <div>
                <p className="eyebrow">Dynamic Form</p>
                <h3>{formSchema.request_type_name}</h3>
              </div>
            </div>

            <DynamicForm
              fields={formSchema.fields}
              values={formValues}
              onChange={handleFieldChange}
              disabled={isSubmitting}
            />

            <button
              className="primary-button"
              type="submit"
              disabled={isSubmitting || !selectedTypeId}
            >
              {isSubmitting ? "Submitting..." : "Submit Request"}
            </button>
          </>
        ) : (
          <div className="empty-state">
            <p>Select a request type to load its form.</p>
          </div>
        )}
      </form>
    </section>
  );
}

export default CreateRequestPage;
