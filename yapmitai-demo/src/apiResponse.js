export function normalizeApiResponse(payload) {
  if (!payload || typeof payload !== "object") return payload;

  const data = payload.data;
  if (data && typeof data === "object" && Array.isArray(data.list)) {
    const { list, ...pagination } = data;
    return {
      ...payload,
      data: list,
      pagination
    };
  }

  return payload;
}

export async function parseApiResponse(response, fallbackMessage = "请求失败") {
  const payload = await response.json().catch(() => ({}));

  if (!response.ok || payload?.success === false) {
    throw new Error(payload?.msg || payload?.detail || `${fallbackMessage}：${response.status}`);
  }

  return normalizeApiResponse(payload);
}
