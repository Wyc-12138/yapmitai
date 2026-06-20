import { API_BASE, API_KEY } from "../apiConfig.js";
import { parseApiResponse } from "../apiResponse.js";

export async function translateTexts(texts) {
  const response = await fetch(`${API_BASE}/translations/batch`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY
    },
    body: JSON.stringify({ texts })
  });

  const payload = await parseApiResponse(response, "翻译请求失败");
  return payload.data?.translations || {};
}
