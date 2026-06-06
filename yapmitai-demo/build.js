import { access } from "node:fs/promises";

const requiredFiles = [
  "index.html",
  "server.js",
  "src/styles.css",
  "src/static-app.js",
  "src/data/mock.js",
  "src/routes/index.js"
];

await Promise.all(requiredFiles.map((file) => access(file)));
const mock = await import("./src/data/mock.js");
const { routes } = await import("./src/routes/index.js");

if (!mock.agents?.length || !mock.tools?.length || !mock.callLogs?.length) {
  throw new Error("Mock data is incomplete.");
}

const expectedRoutes = [
  "/",
  "/enterprise/dashboard",
  "/enterprise/agents",
  "/enterprise/tools",
  "/enterprise/tools/agent-config",
  "/enterprise/tools/agent-logs",
  "/enterprise/creation/agent",
  "/enterprise/outreach/agent",
  "/enterprise/personalwx/agent",
  "/enterprise/corpwx/agent",
  "/enterprise/knowledge/agent",
  "/talent/home",
  "/government/dashboard",
  "/alliance/dashboard"
];

const registeredRoutes = new Set(routes.map((route) => route.path));
const missingRoutes = expectedRoutes.filter((route) => !registeredRoutes.has(route));
if (missingRoutes.length) {
  throw new Error(`Missing frontend routes: ${missingRoutes.join(", ")}`);
}

console.log("Static frontend validation completed.");
