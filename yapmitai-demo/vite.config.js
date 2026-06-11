import { defineConfig } from "vite";
import { join } from "node:path";
import { tmpdir } from "node:os";
import vueSfcPlugin from "./vue-sfc-plugin.js";

export default defineConfig({
  plugins: [vueSfcPlugin()],
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
