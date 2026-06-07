"""Page-oriented backend modules mirroring frontend routes."""

from fastapi import APIRouter

from app.pages.alliance.dashboard.router import router as alliance_dashboard_router
from app.pages.enterprise.agents.router import router as enterprise_agents_router
from app.pages.enterprise.corpwx.agent.router import router as corpwx_agent_router
from app.pages.enterprise.creation.agent.router import router as creation_agent_router
from app.pages.enterprise.dashboard.router import router as enterprise_dashboard_router
from app.pages.enterprise.knowledge.agent.router import router as knowledge_agent_router
from app.pages.enterprise.model_configs.router import router as model_configs_router
from app.pages.enterprise.outreach.agent.router import router as outreach_agent_router
from app.pages.enterprise.personalwx.agent.router import router as personalwx_agent_router
from app.pages.enterprise.tools.agent_config.router import router as agent_config_router
from app.pages.enterprise.tools.agent_logs.router import router as agent_logs_router
from app.pages.enterprise.tools.router import router as tools_center_router
from app.pages.government.dashboard.router import router as government_dashboard_router
from app.pages.talent.home.router import router as talent_home_router

api_router = APIRouter()
api_router.include_router(enterprise_dashboard_router)
api_router.include_router(enterprise_agents_router)
api_router.include_router(tools_center_router)
api_router.include_router(agent_config_router)
api_router.include_router(creation_agent_router)
api_router.include_router(outreach_agent_router)
api_router.include_router(personalwx_agent_router)
api_router.include_router(corpwx_agent_router)
api_router.include_router(knowledge_agent_router)
api_router.include_router(model_configs_router)
api_router.include_router(agent_logs_router)
api_router.include_router(talent_home_router)
api_router.include_router(government_dashboard_router)
api_router.include_router(alliance_dashboard_router)
