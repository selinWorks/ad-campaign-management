from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.record import Record
from app.services.calculate.budget import compute_new_daily_budgets_for_label

router = APIRouter(prefix="/api/calculate", tags=["calculate"])

@router.get("/ping")
def ping():
    return {"ok": True}


@router.post("/", response_model=None)
def calculate_all(db: Session = Depends(get_db)):
    try:
        records = db.query(Record).all()
        if not records:
            raise HTTPException(status_code=404, detail="No records found in database")

        # label bazında grupla
        grouped = {}
        for r in records:
            grouped.setdefault(r.label, []).append(r)

        total_updated = 0

        for label, group in grouped.items():
            # Betül'ün fonksiyonu
            new_budgets = compute_new_daily_budgets_for_label(group)

            for r in group:
                key = (r.campaign_name, r.platform)
                new_daily = new_budgets.get(key, 0.0)

                r.new_daily_budget = new_daily

                # örnek tcpa kuralı (Hira'nın fonksiyonu ile değişecek)
                r.new_target_cpa = round(r.camp_cpa * 0.95, 4) if r.camp_cpa else None

                total_updated += 1

        db.commit()

        return {
            "success": True,
            "updated_records": total_updated,
            "labels_processed": len(grouped),
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))