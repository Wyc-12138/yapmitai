import { API_BASE, API_KEY } from "../../../../apiConfig.js";

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
    throw new Error(payload.msg || payload.detail || `请求失败：${response.status}`);
  }
  return response.json();
}

export const agentsApi = {
  list: () => request("/agents"),
  chatModels: () => request("/agents/chat-models"),
  create: (payload) =>
    request("/agents", { method: "POST", body: JSON.stringify(payload) }),
  update: (id, payload) =>
    request(`/agents/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  delete: (id) => request(`/agents/${id}`, { method: "DELETE" })
};
