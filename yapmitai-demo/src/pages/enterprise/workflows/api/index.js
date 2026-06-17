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

export const workflowsApi = {
  list: () => request("/workflows"),
  teams: () => request("/workflows/team-options"),
  detail: (id) => request(`/workflows/${id}`),
  create: (payload) =>
    request("/workflows", { method: "POST", body: JSON.stringify(payload) }),
  update: (id, payload) =>
    request(`/workflows/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  delete: (id) => request(`/workflows/${id}`, { method: "DELETE" }),
  saveOrder: (id, agentIds) =>
    request(`/workflows/${id}/agent-order`, {
      method: "PUT",
      body: JSON.stringify({ agent_ids: agentIds })
    }),
  run: (id, prompt) =>
    request(`/workflows/${id}/runs`, {
      method: "POST",
      body: JSON.stringify({ prompt })
    }),
  runStatus: (id, runId) => request(`/workflows/${id}/runs/${runId}`),
  async downloadReport(id, runId) {
    const response = await fetch(
      `${API_BASE}/workflows/${id}/runs/${runId}/report`,
      { headers: { "X-API-Key": API_KEY } }
    );
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      throw new Error(payload.msg || payload.detail || "PDF 报告尚未生成");
    }
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `AI工作流报告-${id}.pdf`;
    anchor.click();
    URL.revokeObjectURL(url);
  }
};
