<template>
  <div class="app-shell">
    <aside class="side-nav">
      <button class="brand" @click="router.push(portal.home)">
        <span class="yapmitai-wordmark compact">YAPMITAI</span>
        <small>{{ portal.subtitle }}</small>
      </button>
      <nav>
        <button
          v-for="item in portal.items"
          :key="item.path"
          class="nav-item"
          :class="{ active: route.path === item.path }"
          @click="router.push(item.path)"
        >
          <span class="nav-dot"></span>
          <span>{{ item.label }}<small>{{ item.en }}</small></span>
        </button>
      </nav>
    </aside>

    <main class="main-area">
      <header class="top-bar">
        <div><strong>{{ portal.title }}</strong><span>{{ portal.subtitle }}</span></div>
        <div class="top-actions">
          <button class="ghost-btn" @click="router.push('/')">切换入口</button>
          <button class="primary-btn" @click="router.push(portal.actionPath)">
            {{ portal.actionLabel }}
          </button>
        </div>
      </header>
      <div class="page-content">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const portals = {
  enterprise: {
    title: "企业入口",
    subtitle: "Enterprise Workspace",
    home: "/enterprise/dashboard",
    actionPath: "/enterprise/tools",
    actionLabel: "AI工具中心",
    items: [
      ["/enterprise/dashboard", "企业控制台", "Dashboard"],
      ["/enterprise/agents", "超级AI员工", "Agents"],
      ["/enterprise/tools", "AI工具中心", "Tools"],
      ["/enterprise/knowledge/agent", "企业智库", "Knowledge"],
      ["/enterprise/model-configs", "模型配置", "Models"],
      ["/enterprise/tools/agent-config", "Agent总配置", "Gateway"],
      ["/enterprise/creation/agent", "AI创作配置", "Creation"],
      ["/enterprise/outreach/agent", "AI拓客配置", "Outreach"],
      ["/enterprise/personalwx/agent", "个微Agent", "Personal WX"],
      ["/enterprise/corpwx/agent", "企微Agent", "Corp WX"],
      ["/enterprise/tools/agent-logs", "调用日志", "Logs"]
    ]
  },
  talent: {
    title: "员工入口",
    subtitle: "Talent Workspace",
    home: "/talent/home",
    actionPath: "/talent/home",
    actionLabel: "当前首页",
    items: [["/talent/home", "员工工作台", "Talent"]]
  },
  alliance: {
    title: "联盟入口",
    subtitle: "Alliance Workspace",
    home: "/alliance/dashboard",
    actionPath: "/alliance/dashboard",
    actionLabel: "当前首页",
    items: [["/alliance/dashboard", "产业联盟", "Alliance"]]
  }
};

for (const value of Object.values(portals)) {
  value.items = value.items.map(([path, label, en]) => ({ path, label, en }));
}

const portal = computed(() => {
  if (route.path.startsWith("/talent")) return portals.talent;
  if (route.path.startsWith("/alliance")) return portals.alliance;
  return portals.enterprise;
});
</script>

<style scoped>
</style>
