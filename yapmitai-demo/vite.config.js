import { defineConfig } from "vite";
import { join } from "node:path";
import { tmpdir } from "node:os";
import vueSfcPlugin from "./vue-sfc-plugin.js";

export default defineConfig({
  plugins: [vueSfcPlugin()],
  define: {
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: false,
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false
  },
  cacheDir: join(tmpdir(), "yapmitai-vite-cache"),
  server: {
    host: "0.0.0.0",
    port: 5173
  },
  preview: {
    host: "0.0.0.0",
    port: 5173
  }
});
