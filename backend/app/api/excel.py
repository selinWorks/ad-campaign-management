from __future__ import annotations

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.record import Record
from app.services.excel.reader import read_excel_bytes, validate_required_columns

router = APIRouter(prefix="/api/excel", tags=["excel"])

REQUIRED_COLS = [
    "Campaign name",
    "Labels on Campaign",
]


def _to_float(v):
    try:
        if v is None:
            return None
        if isinstance(v, str):
            v = v.strip().replace(",", ".")
            if v == "":
                return None
        return float(v)
    except Exception:
        return None


def _infer_platform(campaign_name: str | None) -> str | None:
    if not campaign_name:
        return None
    s = campaign_name.lower()
    if "android" in s:
        return "Android"
    if "ios" in s:
        return "iOS"
    if "web" in s:
        return "Web"
    return None


@router.get("/ping")
def ping():
    return {"ok": True}


@router.post("/upload")
async def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx supported")

    file_bytes = await file.read()
    headers, rows = read_excel_bytes(file_bytes)

    missing = validate_required_columns(headers, REQUIRED_COLS)
    if missing:
        raise HTTPException(status_code=422, detail=f"Missing required columns: {missing}")

    inserted = 0
    updated = 0
    skipped = 0

    for row in rows:
        campaign_name = row.get("Campaign name")
        label = row.get("Labels on Campaign")

        if not campaign_name or not label:
            skipped += 1
            continue

        # Upsert by (label, campaign_name)
        rec = (
            db.query(Record)
            .filter(Record.label == str(label), Record.campaign_name == str(campaign_name))
            .first()
        )

        if rec is None:
            rec = Record(label=str(label), campaign_name=str(campaign_name))
            db.add(rec)
            inserted += 1
        else:
            updated += 1

        # ✅ Orijinal header + orijinal satırı sakla (export birebir için)
        rec.source_headers = list(headers)
        rec.raw_row = dict(row)

        # DB field map (calculate için)
        rec.platform = _infer_platform(str(campaign_name))

        rec.camp_budget = _to_float(row.get("Camp. budget"))
        rec.camp_cost = _to_float(row.get("Camp. cost"))
        rec.camp_3d_cost = _to_float(row.get("Camp. 3D cost"))
        rec.camp_conv = _to_float(row.get("Camp. conv."))
        rec.camp_cpa = _to_float(row.get("Camp. CPA"))
        rec.camp_tcpa = _to_float(row.get("Camp. tCPA"))

        rec.mtd_cluster_spend = _to_float(row.get("MTD Cluster Spend"))

        rec.label_budget = _to_float(row.get("Label budget"))
        rec.label_cost = _to_float(row.get("Label cost"))
        rec.label_3d_cost = _to_float(row.get("Label 3D cost"))
        rec.label_conv = _to_float(row.get("Label conv."))
        rec.label_remaining_budget = _to_float(row.get("Label remaining budget"))
        rec.label_kpi_value = _to_float(row.get("Label KPI value"))
        rec.label_cpa = _to_float(row.get("Label CPA"))

    db.commit()

    return {
        "success": True,
        "filename": file.filename,
        "row_count": len(rows),
        "inserted": inserted,
        "updated": updated,
        "skipped": skipped,
    }


@router.get("/debug_routes")
def debug_routes():
    return {"ok": True, "msg": "debug_routes works"}