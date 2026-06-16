const API_BASE = "http://localhost:8000/api/v1";
const API_KEY = "yap_demo_key_2026";

const FIELD_LABELS = {
  name: "团队名称",
  description: "团队说明",
  agent_ids: "AI 员工"
};

function getErrorMessage(payload, status) {
  const issue = Array.isArray(payload?.data) ? payload.data[0] : null;
  if (issue) {
    const field = issue.loc?.[issue.loc.length - 1];
    const label = FIELD_LABELS[field] || field || "请求参数";
    if (issue.type === "string_too_short") {
      return `${label}不能为空`;
    }
    return `${label}：${issue.msg || "格式不正确"}`;
  }
  return payload?.msg || payload?.detail || `请求失败：${status}`;
}

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
    throw new Error(getErrorMessage(payload, response.status));
  }
  return response.json();
}

export const teamsApi = {
  list: () => request("/teams"),
  agentOptions: () => request("/teams/agent-options"),
  summary: () => request("/teams/summary"),
  create: (payload) =>
    request("/teams", { method: "POST", body: JSON.stringify(payload) }),
  update: (id, payload) =>
    request(`/teams/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  delete: (id) => request(`/teams/${id}`, { method: "DELETE" })
};
