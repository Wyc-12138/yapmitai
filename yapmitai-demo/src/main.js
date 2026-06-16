import { createApp } from "vue";
import App from "./App.vue";
import router from "./router/index.js";
import { installRuntimeI18n } from "./i18n/index.js";
import "./styles.css";

createApp(App).use(router).mount("#app");
installRuntimeI18n(document.getElementById("app"));
