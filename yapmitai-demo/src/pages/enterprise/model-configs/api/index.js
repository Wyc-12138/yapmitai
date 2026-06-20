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

  return parseApiResponse(response, "模型配置接口请求失败");
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
