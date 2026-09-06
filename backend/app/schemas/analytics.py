from typing import List, Dict, Any
from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_conversations: int
    active_conversations: int
    escalated_to_human: int
    total_leads: int
    qualified_leads: int
    total_orders: int
    total_revenue: float
    avg_order_value: float
    conversion_rate: float
    ai_handling_rate: float
    avg_response_time_seconds: float


class SalesFunnelStage(BaseModel):
    stage: str
    count: int
    percentage: float


class TopProductStat(BaseModel):
    name: str
    category: str
    inquiries_count: int
    orders_count: int
    revenue: float


class ObjectionStat(BaseModel):
    objection: str
    count: int
    resolved_percentage: float
