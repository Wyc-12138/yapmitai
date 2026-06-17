import { API_BASE, API_KEY } from "../apiConfig.js";

export async function translateTexts(texts) {
  const response = await fetch(`${API_BASE}/translations/batch`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY
    },
    body: JSON.stringify({ texts })
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.msg || payload.detail || `翻译请求失败：${response.status}`);
  }
  const payload = await response.json();
  return payload.data?.translations || {};
}
