import { page, panel, toggle } from "./ui.js";

export function renderModuleConfig(context, config) {
  const source = context.readStore(`${config.type}-agent-source`, "外部Agent");
  return page(config.title, config.en, "模块级独立启停，支持外部Agent、原生模块和关闭三种模式。", `
    ${panel("Agent来源", "Source", `<div class="segmented">${["外部Agent", "原生模块", "关闭"].map((item) => `<button class="${source === item ? "active" : ""}" data-source="${config.type}:${item}">${item}</button>`).join("")}</div>`)}
    <div class="config-list">${config.fields.map((field) => `<article class="config-row"><span>设</span><span>${field}</span>${toggle(source !== "关闭", "noop")}</article>`).join("")}</div>`);
}
