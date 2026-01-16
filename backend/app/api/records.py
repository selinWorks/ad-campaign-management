from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.db import get_db
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordUpdate

# Excel export için beklenen kolon isimleri (upload'dakiyle uyumlu)
DEFAULT_SOURCE_HEADERS = [
    "Campaign name",
    "Labels on Campaign",
    "Camp. budget",
    "Camp. cost",
    "Camp. 3D cost",
    "Camp. conv.",
    "Camp. CPA",
    "Camp. tCPA",
    "MTD Cluster Spend",
    "Label budget",
    "Label cost",
    "Label 3D cost",
    "Label conv.",
    "Label remaining budget",
    "Label KPI value",
    "Label CPA",
]

def _sync_raw_row_from_fields(rec: Record):
    """
    Manuel eklenen/güncellenen kaydı, excel export'un kullandığı raw_row formatına yazar.
    """
    row = dict(rec.raw_row or {})

    row["Campaign name"] = rec.campaign_name
    row["Labels on Campaign"] = rec.label

    row["Camp. budget"] = rec.camp_budget
    row["Camp. cost"] = rec.camp_cost
    row["Camp. 3D cost"] = rec.camp_3d_cost
    row["Camp. conv."] = rec.camp_conv
    row["Camp. CPA"] = rec.camp_cpa
    row["Camp. tCPA"] = rec.camp_tcpa

    row["MTD Cluster Spend"] = rec.mtd_cluster_spend

    row["Label budget"] = rec.label_budget
    row["Label cost"] = rec.label_cost
    row["Label 3D cost"] = rec.label_3d_cost
    row["Label conv."] = rec.label_conv
    row["Label remaining budget"] = rec.label_remaining_budget
    row["Label KPI value"] = rec.label_kpi_value
    row["Label CPA"] = rec.label_cpa

    rec.raw_row = row

    if not rec.source_headers:
        rec.source_headers = list(DEFAULT_SOURCE_HEADERS)


router = APIRouter(prefix="/api/records", tags=["records"])


@router.get("/")
def get_records(db: Session = Depends(get_db)):
    items = db.query(Record).order_by(Record.id.desc()).limit(200).all()

    data = []
    for r in items:
        data.append(
            {
                "id": r.id,
                "label": r.label,
                "campaign_name": r.campaign_name,
                "platform": r.platform,
                "camp_budget": r.camp_budget,
                "camp_cost": r.camp_cost,
                "camp_3d_cost": r.camp_3d_cost,
                "camp_conv": r.camp_conv,
                "camp_cpa": r.camp_cpa,
                "camp_tcpa": r.camp_tcpa,
                "mtd_cluster_spend": r.mtd_cluster_spend,
                "label_budget": r.label_budget,
                "label_cost": r.label_cost,
                "label_3d_cost": r.label_3d_cost,
                "label_conv": r.label_conv,
                "label_remaining_budget": r.label_remaining_budget,
                "label_kpi_value": r.label_kpi_value,
                "label_cpa": r.label_cpa,
                "new_daily_budget": r.new_daily_budget,
                "new_target_cpa": r.new_target_cpa,
            }
        )

    return {"success": True, "count": len(data), "data": data}


@router.post("/")
def create_or_update_record(payload: RecordCreate, db: Session = Depends(get_db)):
    """
    Hocanın isterleri için:
    - Öğretmen yeni kayıt ekleyebilmeli
    - Aynı label + aynı campaign_name varsa yeni eklemek yerine güncelleyebilmeli

    Bu endpoint UPsert yapar.
    """
    data = payload.model_dump()

    existing = (
        db.query(Record)
        .filter(Record.label == data["label"], Record.campaign_name == data["campaign_name"])
        .first()
    )

    if existing:
        for k, v in data.items():
            setattr(existing, k, v)

        _sync_raw_row_from_fields(existing)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Update violates unique constraint (same label + campaign_name).",
            )

        return {"success": True, "created": False, "id": existing.id}

    record = Record(**data)
    db.add(record)
    try:
        db.commit()
        db.refresh(record)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Record already exists (same label + campaign_name).",
        )

    return {"success": True, "created": True, "id": record.id}


@router.patch("/{record_id}")
def update_record(record_id: int, payload: RecordUpdate, db: Session = Depends(get_db)):
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(record, key, value)

    _sync_raw_row_from_fields(record)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Update violates unique constraint (same label + campaign_name).",
        )

    return {"success": True, "id": record.id}

@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()
    return {"success": True, "id": record_id}


@router.get("/ping")
def ping():
    return {"message": "records ok"}