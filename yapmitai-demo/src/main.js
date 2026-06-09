import { computed, createApp, defineComponent, h, onMounted, ref, watch } from "vue";
import { createRouter, createWebHistory, RouterView, useRoute, useRouter } from "vue-router";
import {
  configureAppController,
  handleAppChange,
  handleAppClick,
  initializeApp,
  renderApp
} from "./app-controller.js";
import { routes as pageRoutes } from "./routes/index.js";
import "./styles.css";

const RouteHost = defineComponent({
  name: "RouteHost",
  setup() {
    const route = useRoute();
    const router = useRouter();
    const revision = ref(0);

    configureAppController({
      invalidate: () => {
        revision.value += 1;
      },
      navigate: (path) => router.push(path)
    });

    watch(
      () => route.path,
      () => {
        revision.value += 1;
      }
    );

    onMounted(() => {
      initializeApp();
    });

    const html = computed(() => {
      revision.value;
      return renderApp(route.path);
    });

    return () => h("div", {
      class: "vue-app-root",
      innerHTML: html.value,
      onClick: handleAppClick,
      onChange: handleAppChange
    });
  }
});

const router = createRouter({
  history: createWebHistory(),
  routes: [
    ...pageRoutes.map(({ path }) => ({
      path,
      component: RouteHost
    })),
    {
      path: "/:pathMatch(.*)*",
      component: RouteHost
    }
  ],
  scrollBehavior: () => ({ top: 0 })
});

createApp({
  render: () => h(RouterView)
}).use(router).mount("#app");
