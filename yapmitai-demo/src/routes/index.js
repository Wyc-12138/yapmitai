import home from "../pages/home/index.js";
import allianceDashboard from "../pages/alliance/dashboard/index.js";
import enterpriseAgents from "../pages/enterprise/agents/index.js";
import corpwxAgent from "../pages/enterprise/corpwx/agent/index.js";
import creationAgent from "../pages/enterprise/creation/agent/index.js";
import enterpriseDashboard from "../pages/enterprise/dashboard/index.js";
import knowledgeAgent from "../pages/enterprise/knowledge/agent/index.js";
import outreachAgent from "../pages/enterprise/outreach/agent/index.js";
import personalwxAgent from "../pages/enterprise/personalwx/agent/index.js";
import enterpriseTools from "../pages/enterprise/tools/index.js";
import agentConfig from "../pages/enterprise/tools/agent-config/index.js";
import agentLogs from "../pages/enterprise/tools/agent-logs/index.js";
import governmentDashboard from "../pages/government/dashboard/index.js";
import talentHome from "../pages/talent/home/index.js";

export const routes = [
  home,
  enterpriseDashboard,
  enterpriseAgents,
  enterpriseTools,
  agentConfig,
  agentLogs,
  creationAgent,
  outreachAgent,
  personalwxAgent,
  corpwxAgent,
  knowledgeAgent,
  talentHome,
  governmentDashboard,
  allianceDashboard
];

export function findRoute(pathname) {
  return routes.find((route) => route.path === pathname);
}
