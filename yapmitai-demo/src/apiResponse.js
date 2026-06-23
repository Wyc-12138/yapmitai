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

function formatApiError(payload, fallbackMessage, status) {
  if (payload?.msg) return payload.msg;

  const detail = payload?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === "string") return item;
        const location = Array.isArray(item?.loc) ? item.loc.join(".") : "";
        return [location, item?.msg].filter(Boolean).join(": ");
      })
      .filter(Boolean)
      .join("; ");
  }

  return `${fallbackMessage} (${status})`;
}

export async function parseApiResponse(response, fallbackMessage = "请求失败") {
  const text = await response.text();
  let payload = {};
  try {
    payload = text ? JSON.parse(text) : {};
  } catch {
    if (!response.ok) {
      throw new Error(`${fallbackMessage} (${response.status})`);
    }
    throw new Error("接口返回了无法解析的数据");
  }

  if (!response.ok || payload?.success === false) {
    throw new Error(formatApiError(payload, fallbackMessage, response.status));
  }

  return normalizeApiResponse(payload);
}
