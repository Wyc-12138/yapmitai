const API_BASE = "http://localhost:8000/api/v1";
const API_KEY = "yap_demo_key_2026";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "X-API-Key": API_KEY,
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...options.headers
    }
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.msg || payload.detail || `AI工具接口请求失败：${response.status}`);
  }
  return response.json();
}

export const toolsApi = {
  list(params = {}) {
    const query = new URLSearchParams(params).toString();
    return request(`/tools${query ? `?${query}` : ""}`);
  },
  chatModels: () => request("/tools/chat-models"),
  create: (payload) => request("/tools", { method: "POST", body: JSON.stringify(payload) }),
  update: (id, payload) => request(`/tools/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  delete: (id) => request(`/tools/${id}`, { method: "DELETE" }),
  run: (id, payload) => request(`/tools/${id}/run`, { method: "POST", body: JSON.stringify(payload) })
};
