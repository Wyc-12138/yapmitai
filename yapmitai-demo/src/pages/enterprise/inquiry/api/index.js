import { API_BASE, API_KEY } from "../../../../apiConfig.js";
import { parseApiResponse } from "../../../../apiResponse.js";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "X-API-Key": API_KEY,
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...options.headers
    }
  });
  return parseApiResponse(response, "询盘 AI 请求失败");
}

export const inquiryApi = {
  analyze: (payload) =>
    request("/inquiry/analyze", { method: "POST", body: JSON.stringify(payload) }),
  listHistory: () => request("/inquiry/history"),
  getHistory: (id) => request(`/inquiry/history/${id}`),
  deleteHistory: (id) => request(`/inquiry/history/${id}`, { method: "DELETE" }),
  deleteHistoryBatch: (ids) =>
    request("/inquiry/history/delete", {
      method: "POST",
      body: JSON.stringify({ ids })
    })
};
