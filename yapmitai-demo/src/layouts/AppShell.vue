<template>
  <div class="app-shell" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
    <aside class="side-nav">
      <div class="side-nav-head">
        <button class="brand" title="返回入口首页" @click="router.push(portal.home)">
          <span class="brand-symbol">Y</span>
          <span class="brand-copy">
            <span class="yapmitai-wordmark compact">YAPMITAI</span>
            <small>{{ portal.subtitle }}</small>
          </span>
        </button>
        <button
          class="sidebar-toggle"
          :title="sidebarCollapsed ? '展开侧边栏' : '收起侧边栏'"
          @click="toggleSidebar"
        >
          {{ sidebarCollapsed ? "›" : "‹" }}
        </button>
      </div>

      <nav class="layered-nav">
        <section
          v-for="group in portal.groups"
          :key="group.key"
          class="nav-group"
          :class="{ open: isGroupOpen(group.key), active: groupHasActiveRoute(group) }"
        >
          <button
            class="nav-group-trigger"
            :title="sidebarCollapsed ? group.label : ''"
            @click="toggleGroup(group.key)"
          >
            <span class="nav-group-icon">{{ group.icon }}</span>
            <span class="nav-group-copy">
              <strong>{{ group.label }}</strong>
              <small>{{ group.en }}</small>
            </span>
            <span class="nav-chevron">⌄</span>
          </button>

          <div v-show="!sidebarCollapsed && isGroupOpen(group.key)" class="nav-group-items">
            <button
              v-for="item in group.items"
              :key="item.path"
              class="nav-item"
              :class="{ active: isRouteActive(item.path) }"
              @click="router.push(item.path)"
            >
              <span class="nav-item-icon">{{ item.icon }}</span>
              <span class="nav-item-copy">
                <strong>{{ item.label }}</strong>
                <small>{{ item.en }}</small>
              </span>
            </button>
          </div>
        </section>
      </nav>

      <button class="side-nav-exit" title="切换入口" @click="router.push('/')">
        <span>↗</span>
        <span class="side-nav-exit-copy">切换入口</span>
      </button>
    </aside>

    <main class="main-area">
      <header class="top-bar">
        <div class="top-bar-title">
          <strong>{{ currentPageTitle }}</strong>
          <span>{{ portal.title }} · {{ portal.subtitle }}</span>
        </div>
        <div class="top-actions">
          <button
            class="language-toggle no-translate"
            :title="language === 'zh' ? 'Switch to English' : '切换为中文'"
            @click="toggleLanguage"
          >
            {{ language === "zh" ? "EN" : "中文" }}
          </button>
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
import { computed, reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { language, toggleLanguage } from "../i18n/index.js";

const route = useRoute();
const router = useRouter();

const item = (path, label, en, icon) => ({ path, label, en, icon });
const group = (key, label, en, icon, items) => ({ key, label, en, icon, items });

const portals = {
  enterprise: {
    title: "企业入口",
    subtitle: "Enterprise Workspace",
    home: "/enterprise/dashboard",
    actionPath: "/enterprise/tools",
    actionLabel: "AI工具中心",
    groups: [
      group("overview", "工作总览", "Overview", "⌂", [
        item("/enterprise/dashboard", "企业控制台", "Dashboard", "▦")
      ]),
      group("organization", "AI组织", "AI Organization", "◎", [
        item("/enterprise/agents", "超级AI员工", "Agents", "AI"),
        item("/enterprise/teams", "AI团队", "Teams", "◆"),
        item("/enterprise/workflows", "AI工作流", "Workflows", "⇢")
      ]),
      group("capabilities", "能力中心", "Capabilities", "✦", [
        item("/enterprise/tools", "AI工具中心", "Tools", "◇"),
        item("/enterprise/knowledge/agent", "企业智库", "Knowledge", "▤"),
        item("/enterprise/creation/agent", "AI创作配置", "Creation", "✎"),
        item("/enterprise/outreach/agent", "AI拓客配置", "Outreach", "↑"),
        item("/enterprise/personalwx/agent", "个微Agent", "Personal WX", "私"),
        item("/enterprise/corpwx/agent", "企微Agent", "Corp WX", "企")
      ]),
      group("results", "业务结果", "Business Results", "📊", [
        item("/enterprise/billing", "费用中心", "Billing", "💰"),
        item("/enterprise/tools/agent-logs", "调用日志", "Logs", "≡")
      ]),
      group("system", "系统管理", "System", "⚙", [
        item("/enterprise/energy-center", "AI能源中心", "Energy Center", "⚡"),
        item("/enterprise/model-configs", "模型配置", "Models", "◫"),
        item("/enterprise/tools/agent-config", "Agent总配置", "Gateway", "◉")
      ])
    ]
  },
  talent: {
    title: "员工入口",
    subtitle: "Talent Workspace",
    home: "/talent/home",
    actionPath: "/talent/home",
    actionLabel: "当前首页",
    groups: [
      group("talent", "员工工作", "Talent", "◎", [
        item("/talent/home", "员工工作台", "Talent Workspace", "▦")
      ])
    ]
  },
  alliance: {
    title: "联盟入口",
    subtitle: "Alliance Workspace",
    home: "/alliance/dashboard",
    actionPath: "/alliance/dashboard",
    actionLabel: "当前首页",
    groups: [
      group("alliance", "产业联盟", "Alliance", "◇", [
        item("/alliance/dashboard", "产业联盟", "Alliance Dashboard", "▦")
      ])
    ]
  }
};

const savedCollapsed = window.localStorage.getItem("yapmitai-sidebar-collapsed") === "true";
const sidebarCollapsed = ref(savedCollapsed);
const openGroups = reactive({});

const portal = computed(() => {
  if (route.path.startsWith("/talent")) return portals.talent;
  if (route.path.startsWith("/alliance")) return portals.alliance;
  return portals.enterprise;
});

const flatItems = computed(() => portal.value.groups.flatMap((navGroup) => navGroup.items));
const currentItem = computed(() =>
  [...flatItems.value]
    .sort((left, right) => right.path.length - left.path.length)
    .find(
      (navItem) =>
        route.path === navItem.path || route.path.startsWith(`${navItem.path}/`)
    )
);
const currentPageTitle = computed(() => currentItem.value?.label || portal.value.title);

function isRouteActive(path) {
  return currentItem.value?.path === path;
}

function groupHasActiveRoute(navGroup) {
  return navGroup.items.some((navItem) => isRouteActive(navItem.path));
}

function isGroupOpen(key) {
  return openGroups[key] !== false;
}

function openActiveGroup() {
  for (const navGroup of portal.value.groups) {
    if (!(navGroup.key in openGroups)) {
      openGroups[navGroup.key] = groupHasActiveRoute(navGroup);
    }
    if (groupHasActiveRoute(navGroup)) {
      openGroups[navGroup.key] = true;
    }
  }
}

function toggleSidebar() {
  sidebarCollapsed.value = !sidebarCollapsed.value;
  window.localStorage.setItem(
    "yapmitai-sidebar-collapsed",
    String(sidebarCollapsed.value)
  );
  if (!sidebarCollapsed.value) openActiveGroup();
}

function toggleGroup(key) {
  if (sidebarCollapsed.value) {
    sidebarCollapsed.value = false;
    window.localStorage.setItem("yapmitai-sidebar-collapsed", "false");
    openGroups[key] = true;
    return;
  }
  openGroups[key] = !isGroupOpen(key);
}

watch(
  () => route.path,
  () => openActiveGroup(),
  { immediate: true }
);
</script>

<style scoped>
</style>
