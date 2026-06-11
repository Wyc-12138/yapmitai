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
    throw new Error(payload.msg || payload.detail || `模型配置接口请求失败：${response.status}`);
  }
  return response.json();
}

export function getModelConfigs(params = {}) {
  const query = new URLSearchParams(params).toString();
  return request(`/model-configs${query ? `?${query}` : ""}`);
}

export function createModelConfig(payload) {
  return request("/model-configs", { method: "POST", body: JSON.stringify(payload) });
}

export function updateModelConfig(id, payload) {
  return request(`/model-configs/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
}

export function deleteModelConfig(id) {
  return request(`/model-configs/${id}`, { method: "DELETE" });
}
