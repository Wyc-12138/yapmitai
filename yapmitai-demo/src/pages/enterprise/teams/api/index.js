import { API_BASE, API_KEY } from "../../../../apiConfig.js";
import { normalizeApiResponse } from "../../../../apiResponse.js";

const FIELD_LABELS = {
  name: "团队名称",
  description: "团队说明",
  agent_ids: "AI 员工"
};

function getErrorMessage(payload, status) {
  const issues = Array.isArray(payload?.data)
    ? payload.data
    : Array.isArray(payload?.data?.list)
      ? payload.data.list
      : [];
  const issue = issues[0];

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

  const payload = await response.json().catch(() => ({}));
  if (!response.ok || payload?.success === false) {
    throw new Error(getErrorMessage(payload, response.status));
  }

  return normalizeApiResponse(payload);
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
