import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/", component: () => import("../pages/home/index.vue"), meta: { layout: "full" } },
  { path: "/enterprise/dashboard", component: () => import("../pages/enterprise/dashboard/index.vue") },
  { path: "/enterprise/agents", component: () => import("../pages/enterprise/agents/index.vue") },
  { path: "/enterprise/tools", component: () => import("../pages/enterprise/tools/index.vue") },
  { path: "/enterprise/tools/agent-config", component: () => import("../pages/enterprise/tools/agent-config/index.vue") },
  { path: "/enterprise/tools/agent-logs", component: () => import("../pages/enterprise/tools/agent-logs/index.vue") },
  { path: "/enterprise/creation/agent", component: () => import("../pages/enterprise/creation/agent/index.vue") },
  { path: "/enterprise/outreach/agent", component: () => import("../pages/enterprise/outreach/agent/index.vue") },
  { path: "/enterprise/personalwx/agent", component: () => import("../pages/enterprise/personalwx/agent/index.vue") },
  { path: "/enterprise/corpwx/agent", component: () => import("../pages/enterprise/corpwx/agent/index.vue") },
  { path: "/enterprise/knowledge/agent", component: () => import("../pages/enterprise/knowledge/agent/index.vue") },
  { path: "/enterprise/model-configs", component: () => import("../pages/enterprise/model-configs/index.vue") },
  { path: "/talent/home", component: () => import("../pages/talent/home/index.vue") },
  { path: "/government/dashboard", component: () => import("../pages/government/dashboard/index.vue"), meta: { layout: "full" } },
  { path: "/alliance/dashboard", component: () => import("../pages/alliance/dashboard/index.vue") },
  { path: "/:pathMatch(.*)*", redirect: "/" }
];

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
});
