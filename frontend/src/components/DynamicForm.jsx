function getSelectOptions(options) {
  if (!Array.isArray(options)) {
    return [];
  }

  return options.map((option) => {
    if (typeof option === "object" && option !== null) {
      return {
        label: option.label ?? option.name ?? String(option.value ?? ""),
        value: option.value ?? option.id ?? option.name ?? ""
      };
    }

    return {
      label: String(option),
      value: String(option)
    };
  });
}

function DynamicForm({ fields, values, onChange, disabled = false }) {
  if (!fields?.length) {
    return (
      <div className="empty-state subtle">
        <p>No dynamic fields are configured for this request type.</p>
      </div>
    );
  }

  return (
    <div className="dynamic-grid">
      {fields.map((field) => {
        const value = values[field.name];
        const commonProps = {
          id: field.name,
          name: field.name,
          disabled,
          required: field.is_required,
          placeholder: field.placeholder || "",
          className: "input-control"
        };

        let control = null;

        switch (field.field_type) {
          case "TEXT":
            control = (
              <input
                {...commonProps}
                type="text"
                value={value ?? ""}
                onChange={(event) => onChange(field.name, event.target.value)}
              />
            );
            break;

          case "TEXTAREA":
            control = (
              <textarea
                {...commonProps}
                rows="4"
                value={value ?? ""}
                onChange={(event) => onChange(field.name, event.target.value)}
              />
            );
            break;

          case "NUMBER":
            control = (
              <input
                {...commonProps}
                type="number"
                value={value ?? ""}
                onChange={(event) =>
                  onChange(
                    field.name,
                    event.target.value === "" ? "" : Number(event.target.value)
                  )
                }
              />
            );
            break;

          case "DATE":
            control = (
              <input
                {...commonProps}
                type="date"
                value={value ?? ""}
                onChange={(event) => onChange(field.name, event.target.value)}
              />
            );
            break;

          case "DATETIME":
            control = (
              <input
                {...commonProps}
                type="datetime-local"
                value={value ?? ""}
                onChange={(event) => onChange(field.name, event.target.value)}
              />
            );
            break;

          case "BOOLEAN":
            control = (
              <label className="checkbox-row" htmlFor={field.name}>
                <input
                  id={field.name}
                  name={field.name}
                  type="checkbox"
                  checked={Boolean(value)}
                  disabled={disabled}
                  onChange={(event) => onChange(field.name, event.target.checked)}
                />
                <span>{field.label}</span>
              </label>
            );
            break;

          case "SELECT":
            control = (
              <select
                {...commonProps}
                value={value ?? ""}
                onChange={(event) => onChange(field.name, event.target.value)}
              >
                <option value="">Choose an option</option>
                {getSelectOptions(field.options).map((option) => (
                  <option key={`${field.name}-${option.value}`} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            );
            break;

          case "FILE":
            control = (
              <div className="file-control">
                <input
                  id={field.name}
                  name={field.name}
                  type="file"
                  disabled={disabled}
                  className="input-control"
                  onChange={(event) => {
                    const file = event.target.files?.[0];
                    onChange(
                      field.name,
                      file
                        ? {
                            name: file.name,
                            size: file.size,
                            type: file.type
                          }
                        : null
                    );
                  }}
                />
                <p className="field-hint">Stored as file metadata because the backend accepts JSON payloads.</p>
              </div>
            );
            break;

          default:
            control = (
              <input
                {...commonProps}
                type="text"
                value={value ?? ""}
                onChange={(event) => onChange(field.name, event.target.value)}
              />
            );
        }

        return (
          <div key={field.name} className="field-block">
            {field.field_type !== "BOOLEAN" ? (
              <label className="field-label" htmlFor={field.name}>
                {field.label}
                {field.is_required ? <span className="required-mark"> *</span> : null}
              </label>
            ) : null}
            {control}
          </div>
        );
      })}
    </div>
  );
}

export default DynamicForm;
