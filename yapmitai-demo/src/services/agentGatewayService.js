const agentPackages = [
  { id: "creation-image", name: "文生图 Agent", type: "AI创作", version: "1.2.0", enabled: true },
  { id: "creation-video", name: "文生视频 Agent", type: "AI创作", version: "1.0.8", enabled: true },
  { id: "outreach-leads", name: "智能获客 Agent", type: "拓客", version: "2.1.1", enabled: true },
  { id: "cs-personalwx", name: "个微客服 Agent", type: "客服", version: "1.4.3", enabled: false },
  { id: "cs-corpwx", name: "企微客服 Agent", type: "客服", version: "1.5.0", enabled: true },
  { id: "knowledge-rag", name: "RAG知识库 Agent", type: "知识库", version: "0.9.7", enabled: true }
];

export const agentGatewayService = {
  getAgentList() {
    return agentPackages;
  },
  toggleAgent(agentId, enabled) {
    return { code: 200, data: { agentId, enabled }, msg: "success", traceId: crypto.randomUUID() };
  },
  callAgent(agentId, params) {
    return {
      code: 200,
      data: { agentId, params, fallback: false, result: "mock agent result" },
      msg: "success",
      traceId: crypto.randomUUID()
    };
  },
  getCallLogs() {
    return { code: 200, data: [], msg: "success", traceId: crypto.randomUUID() };
  },
  getStatsOverview() {
    return {
      code: 200,
      data: { calls: 1248, successRate: 98.6, latency: 1280, cost: 8420 },
      msg: "success",
      traceId: crypto.randomUUID()
    };
  }
};
