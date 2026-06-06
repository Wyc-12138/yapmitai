import { renderModuleConfig } from "../../../../shared/module-config.js";

export default {
  path: "/enterprise/corpwx/agent",
  layout: "shell",
  render(context) {
    return renderModuleConfig(context, {
      type: "corpwx",
      title: "AI企微Agent配置",
      en: "Enterprise WeChat Agent",
      fields: ["部门归属：海外销售部", "接管模式：全托管", "关键词问答：外部知识库优先", "工单升级：开启"]
    });
  }
};
