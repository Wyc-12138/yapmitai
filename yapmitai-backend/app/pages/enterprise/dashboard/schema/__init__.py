from pydantic import BaseModel


class DashboardOverview(BaseModel):
    kpis: list[dict]
    sales_trend: list[dict]
    task_distribution: list[dict]
    tasks: list[dict]
    gateway_stats: dict
