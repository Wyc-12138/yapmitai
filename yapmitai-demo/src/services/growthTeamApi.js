const API_BASE = "http://localhost:8000/api/task";
const API_KEY = "yap_demo_key_2026";

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
        ...options.headers
      }
    });
  } catch (error) {
    if (error?.message === "Failed to fetch") {
      throw new Error("无法连接后端，请确认已启动：python -m uvicorn app.main:app --host 127.0.0.1 --port 8000");
    }
    throw error;
  }
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.msg || payload.detail || `请求失败（${response.status}）`);
  }
  if (options.raw) return response;
  return response.json();
}

export const growthTeamApi = {
  startTask(prompt) {
    return request("/start", {
      method: "POST",
      body: JSON.stringify({ prompt })
    });
  },
  getTask(taskId) {
    return request(`/${taskId}`);
  },
  async downloadReport(taskId) {
    const response = await request(`/${taskId}/report`, { raw: true });
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `Growth-Strategy-Report-${taskId}.pdf`;
    link.click();
    URL.revokeObjectURL(url);
  }
};
