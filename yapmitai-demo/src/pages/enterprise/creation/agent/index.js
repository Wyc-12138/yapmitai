import { renderModuleConfig } from "../../../../shared/module-config.js";

export default {
  path: "/enterprise/creation/agent",
  layout: "shell",
  render(context) {
    return renderModuleConfig(context, {
      type: "creation",
      title: "AI创作模块配置",
      en: "Creation Agent Config",
      fields: ["文生图风格：商业摄影 / 3D渲染 / 国潮插画", "文生视频：15s / 30s / 60s", "多模态输入：图+文 / 文+表", "水印开关：开启"]
    });
  }
};
