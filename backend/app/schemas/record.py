from pydantic import BaseModel
from typing import Optional


class RecordCreate(BaseModel):
    label: str
    campaign_name: str
    platform: str

    camp_budget: Optional[float] = None
    camp_cost: Optional[float] = None
    camp_3d_cost: Optional[float] = None
    camp_conv: Optional[float] = None
    camp_cpa: Optional[float] = None
    camp_tcpa: Optional[float] = None
    mtd_cluster_spend: Optional[float] = None

    label_budget: Optional[float] = None
    label_cost: Optional[float] = None
    label_3d_cost: Optional[float] = None
    label_conv: Optional[float] = None
    label_remaining_budget: Optional[float] = None
    label_kpi_value: Optional[float] = None
    label_cpa: Optional[float] = None


class RecordUpdate(BaseModel):
    label: Optional[str] = None
    campaign_name: Optional[str] = None
    platform: Optional[str] = None

    camp_budget: Optional[float] = None
    camp_cost: Optional[float] = None
    camp_3d_cost: Optional[float] = None
    camp_conv: Optional[float] = None
    camp_cpa: Optional[float] = None
    camp_tcpa: Optional[float] = None
    mtd_cluster_spend: Optional[float] = None

    label_budget: Optional[float] = None
    label_cost: Optional[float] = None
    label_3d_cost: Optional[float] = None
    label_conv: Optional[float] = None
    label_remaining_budget: Optional[float] = None
    label_kpi_value: Optional[float] = None
    label_cpa: Optional[float] = None

    new_daily_budget: Optional[float] = None
    new_target_cpa: Optional[float] = None