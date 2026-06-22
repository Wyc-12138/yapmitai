const RESPONSES = {
  品牌: "在品牌增长场景中，YAPMIT AI 通过三步提升效率：① 品牌知识库沉淀，确保所有内容风格一致；② 多 Agent 协同生产，从策略到发布全自动；③ 效果数据闭环，高效内容模式自动沉淀复用。平均可将内容生产效率提升 73% 以上。",
  跨境: "跨境出海的核心风险集中在三个环节：① 合规风险——不同国家海关法规、产品认证要求差异大；② 本地化风险——文案直译导致文化误读；③ 汇率与定价风险——汇率波动侵蚀利润。YAPMIT 跨境 AI 针对这三点均有专属 Agent 模块覆盖，支持 50+ 目标市场。",
  招商: "招商工作的 AI 赋能重点在于：① 企业精准筛选——从百万企业库中按产业方向、规模、注册地多维匹配，效率提升 3 倍；② 材料自动化——针对不同企业自动生成定制化招商材料；③ 全流程 CRM——从意向到落地的每个节点自动追踪提醒，防止线索流失。",
  agent: "YAPMIT 的 Agent Team 采用多智能体协同架构——每个 Agent 承担特定角色（如策略 Agent、内容 Agent、合规 Agent），通过 Workflow Studio 编排协作。不同 Agent 共享同一知识库（Skills），并可调用各类工具（Tools），最终由底层模型执行推理，Compute Center 负责算力调度。",
  文旅: "导购文旅空间融合了两大核心能力：① 智能导购——基于用户偏好实时推荐商品与活动，带动消费转化提升 35%；② 文旅服务——从行程规划到多语言导览，AI 全旅程陪伴。适合景区、OTA、商业综合体、免税店等场景接入。",
  default: "这是个很好的问题！YAPMIT AI OS 围绕四大行业空间构建——品牌增长、跨境出海、导购文旅、招商引资。每个空间都有专属的 Agent Team 和 Skill 库。你可以进一步问我具体场景，我来为你详细解答。"
};

export function getAskMeReply(text) {
  const t = text;
  if (t.includes("品牌") || t.includes("内容") || t.includes("营销") || t.includes("marketing")) return RESPONSES["品牌"];
  if (t.includes("跨境") || t.includes("出海") || t.includes("合规") || t.includes("cross")) return RESPONSES["跨境"];
  if (t.includes("招商") || t.includes("政府") || t.includes("园区") || t.includes("investment")) return RESPONSES["招商"];
  if (t.includes("agent") || t.includes("智能体") || t.includes("工作流") || t.includes("架构")) return RESPONSES["agent"];
  if (t.includes("文旅") || t.includes("旅游") || t.includes("导购") || t.includes("commerce")) return RESPONSES["文旅"];
  return RESPONSES.default;
}

export const askMeChips = [
  "如何用 AI 提升品牌内容效率？",
  "跨境出海合规有哪些关键风险？",
  "政府招商如何精准锁定目标企业？",
  "YAPMIT 的 Agent Team 怎么工作？"
];
