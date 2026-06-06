import { stats } from "../../data/mock.js";
import { metric } from "../../shared/ui.js";

export default {
  path: "/",
  layout: "full",
  render() {
    const entrances = [
      ["/talent/home", "员工入口", "Talent", "160万职工AI工作台", "人"],
      ["/enterprise/dashboard", "企业入口", "Enterprise", "AI增长平台与超级员工", "企"],
      ["/government/dashboard", "政府入口", "Government", "产业AI决策驾驶舱", "政"],
      ["/alliance/dashboard", "联盟入口", "Alliance", "品牌增长计划网络", "盟"]
    ];
    return `
      <div class="login-page">
        <div class="mesh-bg"></div>
        <header class="login-header">
          <button class="brand on-hero" data-go="/"><span class="brand-mark">Y</span><span><strong>悦普AI产业超级操作系统</strong><small>YAPMITAI Industrial AI OS</small></span></button>
          <span class="pill">Public Demo Online</span>
        </header>
        <section class="login-hero">
          <div class="hero-copy"><span class="eyebrow">Demo v2.0 · AI产业基础设施</span><h1>面向员工、企业、政府与产业联盟的 AI 产业超级操作系统</h1><p>企业像管理团队一样雇佣AI员工，政府看到产业运行数据，联盟推动品牌增长计划。</p></div>
          <div class="entrance-grid">${entrances.map(([path, label, en, desc, icon], index) => `<button class="entrance-card" data-go="${path}" style="animation-delay:${index * 90}ms"><span class="tool-icon">${icon}</span><strong>${label}</strong><small>${en}</small><span>${desc}</span><span class="corner-icon">›</span></button>`).join("")}</div>
        </section>
        <section class="stats-strip">${stats.map(metric).join("")}</section>
      </div>`;
  }
};
