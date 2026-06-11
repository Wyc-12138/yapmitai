<template>
  <div class="landing-page">
    <header class="landing-nav">
      <button class="brand light-brand" @click="router.push('/')"><span class="yapmitai-wordmark">YAPMITAI</span></button>
      <nav class="landing-menu">
        <div v-for="portal in portals" :key="portal.label" class="landing-menu-item">
          <button @click="router.push(portal.path)">{{ portal.label }}</button>
          <div class="landing-mega">
            <button v-for="(page, index) in portal.pages" :key="page.path" :class="{ featured: index === 0 }" @click="router.push(page.path)">
              <strong>{{ page.title }}</strong><span>{{ page.description }}</span>
            </button>
          </div>
        </div>
      </nav>
      <button class="landing-login" @click="router.push('/enterprise/dashboard')">进入系统</button>
    </header>
    <section class="landing-hero">
      <div class="landing-copy">
        <span class="landing-kicker">YAPMITAI Demo v2.0</span>
        <h1>悦普AI产业超级操作系统</h1>
        <p>四个入口，四套边界。企业管理 AI 员工与工具，员工完成日常任务，政府查看产业态势，联盟推进品牌增长。</p>
        <div class="landing-actions"><button class="primary-btn" @click="router.push('/enterprise/dashboard')">开始使用</button><button class="ghost-btn" @click="router.push('/enterprise/tools')">查看AI工具</button></div>
      </div>
      <div class="landing-visual" aria-hidden="true">
        <div class="visual-window"><div class="visual-question">What should the team focus on this week?</div><div class="visual-content"><section><span>Summary</span><strong>AI contribution is rising across tools and knowledge workflows.</strong><div class="visual-chart"><i v-for="n in 5" :key="n"></i></div></section><section><span>Recommendations</span><p>Prioritize customer reply automation.</p><p>Connect local knowledge bases.</p><p>Review model costs weekly.</p></section></div><div class="visual-input">Ask a follow-up question <b>Ask</b></div></div>
      </div>
    </section>
    <section class="portal-grid">
      <button v-for="(portal, index) in portals" :key="portal.path" class="portal-card" :style="{ animationDelay: `${index * 70}ms` }" @click="router.push(portal.path)">
        <span>{{ portal.icon }}</span><strong>{{ portal.title }}</strong><small>{{ portal.en }}</small><p>{{ portal.desc }}</p><em>{{ portal.scope }}</em>
      </button>
    </section>
  </div>
</template>
<script setup>
import { useRouter } from "vue-router";
const router = useRouter();
const portals = [
  { path: "/enterprise/dashboard", label: "企业", title: "企业入口", en: "Enterprise", desc: "AI增长平台与超级员工", icon: "企", scope: "经营、工具、知识库、模型配置", pages: [
    { path: "/enterprise/dashboard", title: "企业控制台", description: "查看经营指标、任务队列与AI贡献。" },
    { path: "/enterprise/agents", title: "超级AI员工", description: "像管理团队一样管理AI员工。" },
    { path: "/enterprise/tools", title: "AI工具中心", description: "使用Prompt Skills完成业务任务。" },
    { path: "/enterprise/knowledge/agent", title: "企业智库", description: "管理本地知识库与RAG问答。" },
    { path: "/enterprise/model-configs", title: "模型配置", description: "配置Chat和Embedding模型。" },
    { path: "/enterprise/tools/agent-config", title: "Agent总配置", description: "管理网关、模块和连接测试。" },
    { path: "/enterprise/creation/agent", title: "AI创作配置", description: "配置图片、视频和内容生成能力。" },
    { path: "/enterprise/tools/agent-logs", title: "调用日志", description: "查看接口、模型调用和异常。" }
  ]},
  { path: "/talent/home", label: "员工", title: "员工入口", en: "Talent", desc: "个人AI工作台", icon: "人", scope: "任务、助手、个人效率", pages: [{ path: "/talent/home", title: "员工工作台", description: "处理日常任务并使用个人AI助手。" }] },
  { path: "/government/dashboard", label: "政府", title: "政府入口", en: "Government", desc: "产业AI决策驾驶舱", icon: "政", scope: "产业运行、政策问答、宏观指标", pages: [{ path: "/government/dashboard", title: "政府驾驶舱", description: "查看产业运行、企业分布和政策问答。" }] },
  { path: "/alliance/dashboard", label: "联盟", title: "联盟入口", en: "Alliance", desc: "品牌增长计划网络", icon: "盟", scope: "成员协同、增长计划、联盟看板", pages: [{ path: "/alliance/dashboard", title: "产业联盟", description: "管理联盟成员和品牌增长计划。" }] }
];
</script>
<style scoped></style>
