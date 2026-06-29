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
            <div
              v-for="item in group.items"
              :key="item.key || item.path || item.label"
              class="nav-item-block"
            >
              <button
                class="nav-item"
                :class="{
                  active: isItemActive(item),
                  disabled: item.disabled,
                  'has-children': item.children?.length
                }"
                :disabled="item.disabled"
                @click="handleItemClick(item)"
              >
                <span class="nav-item-icon">{{ item.icon }}</span>
                <span class="nav-item-copy">
                  <strong>{{ item.label }}</strong>
                  <small>{{ item.en }}</small>
                </span>
                <span v-if="item.badge" class="nav-item-badge">{{ item.badge }}</span>
              </button>

              <div v-if="item.children?.length" class="nav-subitems">
                <button
                  v-for="child in item.children"
                  :key="child.key || child.path || child.label"
                  class="nav-item nav-subitem"
                  :class="{ active: isItemActive(child), disabled: child.disabled }"
                  :disabled="child.disabled"
                  @click="handleItemClick(child)"
                >
                  <span class="nav-item-icon">{{ child.icon }}</span>
                  <span class="nav-item-copy">
                    <strong>{{ child.label }}</strong>
                    <small>{{ child.en }}</small>
                  </span>
                  <span v-if="child.badge" class="nav-item-badge">{{ child.badge }}</span>
                </button>
              </div>
            </div>
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
          <span class="top-date">{{ headerDate }}</span>
          <button class="top-action-btn" @click="router.push('/enterprise/tools/agent-logs')">
            调用日志
          </button>
          <button class="top-action-btn" disabled>
            导出报告
          </button>
          <button class="top-action-primary" @click="createTask">
            + 新增任务
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

const route = useRoute();
const router = useRouter();

const item = (path, label, en, icon, options = {}) => ({ path, label, en, icon, ...options });
const group = (key, label, en, icon, items) => ({ key, label, en, icon, items });
const comingSoon = (label, en, icon) =>
  item(null, label, en, icon, { disabled: true, badge: "Coming Soon" });

const portals = {
  enterprise: {
    title: "企业入口",
    subtitle: "Enterprise Workspace",
    home: "/enterprise/dashboard",
    actionPath: "/enterprise/tools",
    actionLabel: "AI工具中心",
    groups: [
      group("overview", "总览", "Overview", "O", [
        item("/enterprise/dashboard", "控制台", "Dashboard", "D"),
        comingSoon("任务", "Tasks", "T"),
        item("/enterprise/workflows", "工作流", "Workflow Studio", "W")
      ]),
      group("workforce", "AI 劳动力", "Workforce", "W", [
        item("/enterprise/agents", "AI 员工", "AI Employees", "AI"),
        item("/enterprise/teams", "AI 团队", "AI Teams", "T"),
        item("/enterprise/knowledge/agent", "知识库", "Knowledge Base", "K")
      ]),
      group("business", "业务", "Business", "B", [
        comingSoon("数据分析", "Analytics", "A"),
        item("/enterprise/inquiry", "询盘AI", "Inquiry AI", "I"),
        comingSoon("拓客中心", "Leads", "L"),
        comingSoon("报告", "Reports", "R"),
        item("/enterprise/billing", "成本中心", "Cost Center", "C")
      ]),
      group("infrastructure", "基础设施", "Infrastructure", "I", [
        item("/enterprise/tools", "工具箱", "Toolbox", "T"),
        item("/enterprise/model-configs", "模型", "Models", "M"),
        comingSoon("集成", "Integrations", "I"),
        item(null, "设置", "Settings", "S", {
          key: "settings",
          children: [
            item("/enterprise/tools/agent-config", "Agent 总配置", "Agent Config", "A"),
            item("/enterprise/tools/agent-logs", "调用日志", "Logs", "L"),
            item("/enterprise/energy-center", "AI 能源中心", "Energy Center", "E"),
            comingSoon("通用配置", "General Settings", "G")
          ]
        })
      ]),
      group("portals", "入口", "Portals", "P", [
        item("/talent/home", "员工入口", "Employee Portal", "E"),
        item("/government/dashboard", "政府入口", "Government Portal", "G"),
        item("/alliance/dashboard", "联盟入口", "Alliance Portal", "A")
      ]),
      group("future", "未来功能", "Future", "F", [
        comingSoon("计算中心", "Compute Center", "C"),
        comingSoon("Agent 市场", "Agent Marketplace", "A"),
        comingSoon("模型中心", "Model Hub", "M"),
        comingSoon("API 网关", "API Gateway", "G")
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

function flattenItems(items) {
  return items.flatMap((navItem) => [
    navItem,
    ...(navItem.children ? flattenItems(navItem.children) : [])
  ]);
}

const flatItems = computed(() => portal.value.groups.flatMap((navGroup) => flattenItems(navGroup.items)));
const currentItem = computed(() =>
  [...flatItems.value]
    .filter((navItem) => navItem.path)
    .sort((left, right) => right.path.length - left.path.length)
    .find(
      (navItem) =>
        route.path === navItem.path || route.path.startsWith(`${navItem.path}/`)
    )
);
const currentPageTitle = computed(() => currentItem.value?.label || portal.value.title);
const headerDate = computed(() => {
  const date = new Date();
  const weekday = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"][date.getDay()];
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}.${month}.${day} ${weekday}`;
});

function isRouteActive(path) {
  return Boolean(path) && currentItem.value?.path === path;
}

function isItemActive(navItem) {
  return (
    isRouteActive(navItem.path) ||
    Boolean(navItem.children?.some((child) => isItemActive(child)))
  );
}

function groupHasActiveRoute(navGroup) {
  return navGroup.items.some((navItem) => isItemActive(navItem));
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

function handleItemClick(navItem) {
  if (navItem.disabled || !navItem.path) return;
  router.push(navItem.path);
}

function createTask() {
  router.push({ path: "/enterprise/workflows", query: { create: "1" } });
}

watch(
  () => route.path,
  () => openActiveGroup(),
  { immediate: true }
);
</script>

<style scoped>
</style>
