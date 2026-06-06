import { renderModuleConfig } from "../../../../shared/module-config.js";

export default {
  path: "/enterprise/personalwx/agent",
  layout: "shell",
  render(context) {
    return renderModuleConfig(context, {
      type: "personalwx",
      title: "AI个微Agent配置",
      en: "Personal WeChat Agent",
      fields: ["接管模式：AI建议+人工确认", "关键词问答：合并检索", "SOP群发：限频开启", "客户标签：自动识别"]
    });
  }
};
