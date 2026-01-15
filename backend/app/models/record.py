from sqlalchemy import Column, Integer, String, Float, UniqueConstraint, JSON
from app.core.db import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)

    # Unique key (hocanın istediği "aynı label + aynı campaign update")
    label = Column(String, nullable=False, index=True)
    campaign_name = Column(String, nullable=False, index=True)

    platform = Column(String, nullable=True, index=True)

    # Excel metrikleri
    camp_budget = Column(Float, nullable=True)
    camp_cost = Column(Float, nullable=True)
    camp_3d_cost = Column(Float, nullable=True)
    camp_conv = Column(Float, nullable=True)
    camp_cpa = Column(Float, nullable=True)
    camp_tcpa = Column(Float, nullable=True)

    mtd_cluster_spend = Column(Float, nullable=True)

    label_budget = Column(Float, nullable=True)
    label_cost = Column(Float, nullable=True)
    label_3d_cost = Column(Float, nullable=True)
    label_conv = Column(Float, nullable=True)
    label_remaining_budget = Column(Float, nullable=True)
    label_kpi_value = Column(Float, nullable=True)
    label_cpa = Column(Float, nullable=True)

    # Hesaplanan kolonlar (DB field)
    new_daily_budget = Column(Float, nullable=True)
    new_target_cpa = Column(Float, nullable=True)

    # ✅ Orijinal Excel başlık + satır (export için birebir)
    source_headers = Column(JSON, nullable=True)  # list[str] (sıra önemli)
    raw_row = Column(JSON, nullable=True)         # dict: {orijinal_header: value}

    __table_args__ = (
        UniqueConstraint("label", "campaign_name", name="uq_label_campaign"),
    )