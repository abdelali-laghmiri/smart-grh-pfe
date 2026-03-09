function StatusBadge({ value }) {
  const tone = value ? `status-badge status-${value.toLowerCase()}` : "status-badge";

  return <span className={tone}>{value || "UNKNOWN"}</span>;
}

export default StatusBadge;
