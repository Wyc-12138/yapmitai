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

  return parseApiResponse(response, "AI工具接口请求失败");
}

export const demoMediaApi = {
  textToImage: (payload) =>
    request("/demo-media/text-to-image", { method: "POST", body: JSON.stringify(payload) }),
  textToVideo: (payload) =>
    request("/demo-media/text-to-video", { method: "POST", body: JSON.stringify(payload) }),
  getVideoStatus: (taskId) => request(`/demo-media/video-status/${taskId}`)
};

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
