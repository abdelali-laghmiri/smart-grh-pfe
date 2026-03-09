const API_BASE_URL = import.meta.env.VITE_API_URL || "/api";
const TOKEN_KEY = "smart-grh-token";

export class ApiError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

export const tokenStorage = {
  get() {
    return localStorage.getItem(TOKEN_KEY);
  },
  set(token) {
    localStorage.setItem(TOKEN_KEY, token);
  },
  clear() {
    localStorage.removeItem(TOKEN_KEY);
  }
};

async function parseResponse(response) {
  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const data = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    if (response.status === 401) {
      tokenStorage.clear();
    }

    const detail =
      typeof data === "object" && data !== null
        ? data.detail || data.message
        : data;

    throw new ApiError(detail || "Request failed", response.status, data);
  }

  return data;
}

async function request(path, options = {}) {
  const {
    method = "GET",
    body,
    headers = {},
    auth = true,
    isForm = false
  } = options;

  const nextHeaders = new Headers(headers);

  if (auth) {
    const token = tokenStorage.get();

    if (token) {
      nextHeaders.set("Authorization", `Bearer ${token}`);
    }
  }

  let payload = body;

  if (body !== undefined && body !== null && !isForm && !(body instanceof FormData)) {
    nextHeaders.set("Content-Type", "application/json");
    payload = JSON.stringify(body);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: nextHeaders,
    body: payload
  });

  return parseResponse(response);
}

export const api = {
  login({ matricule, password }) {
    const formData = new URLSearchParams();
    formData.set("username", matricule);
    formData.set("password", password);

    return request("/auth/login", {
      method: "POST",
      body: formData,
      auth: false,
      isForm: true,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      }
    });
  },

  getCurrentUser() {
    return request("/auth/me");
  },

  getRequestTypes() {
    return request("/requests/types");
  },

  getRequestForm(typeId) {
    return request(`/requests/types/${typeId}/form`);
  },

  getMyRequests() {
    return request("/requests/my");
  },

  getApprovals() {
    return request("/requests/approvals");
  },

  createRequest(payload) {
    return request("/requests", {
      method: "POST",
      body: payload
    });
  },

  approveRequest(requestId, comment) {
    return request(`/requests/${requestId}/approve`, {
      method: "POST",
      body: { comment: comment || null }
    });
  },

  rejectRequest(requestId, comment) {
    return request(`/requests/${requestId}/reject`, {
      method: "POST",
      body: { comment: comment || null }
    });
  }
};
