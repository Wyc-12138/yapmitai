const API_BASE = "http://localhost:8000/api/v1";
const API_KEY = "yap_demo_key_2026";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "X-API-Key": API_KEY,
      ...(options.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...options.headers
    }
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.msg || payload.detail || `知识库接口请求失败：${response.status}`);
  }
  return response.json();
}

export const knowledgeApi = {
  getModelConfig(knowledgeBaseId) {
    const query = knowledgeBaseId ? `?knowledge_base_id=${encodeURIComponent(knowledgeBaseId)}` : "";
    return request(`/knowledge/model-config${query}`);
  },
  updateModelConfig: (payload) => request("/knowledge/model-config", { method: "PUT", body: JSON.stringify(payload) }),
  testModels: (payload) => request("/knowledge/model-test", { method: "POST", body: JSON.stringify(payload) }),
  query: (payload) => request("/knowledge/query", { method: "POST", body: JSON.stringify(payload) }),
  listLibraries(params = {}) {
    const query = new URLSearchParams(params).toString();
    return request(`/knowledge/local-libraries${query ? `?${query}` : ""}`);
  },
  createLibrary: (payload) => request("/knowledge/local-libraries", { method: "POST", body: JSON.stringify(payload) }),
  getLibrary: (id) => request(`/knowledge/local-libraries/${id}`),
  updateLibrary: (id, payload) => request(`/knowledge/local-libraries/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  deleteLibrary: (id) => request(`/knowledge/local-libraries/${id}`, { method: "DELETE" }),
  uploadCollection(id, file) {
    const form = new FormData();
    form.append("file", file);
    return request(`/knowledge/local-libraries/${id}/collections`, { method: "POST", body: form });
  }
};
