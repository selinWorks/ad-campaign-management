print("### LOADED: app/api/excel.py ###")
print("### HAS UPLOAD ENDPOINT ###")

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.excel.reader import read_excel_bytes, validate_required_columns
from app.core.db import SessionLocal
from app.models.record import Record

router = APIRouter(prefix="/api/excel", tags=["excel"])

REQUIRED_COLUMNS = [
    "Campaign name",
    "Labels on Campaign",
]

EXCEL_TO_MODEL = {
    "Camp. budget": "camp_budget",
    "Camp. cost": "camp_cost",
    "Camp. 3D cost": "camp_3d_cost",
    "Camp. conv.": "camp_conv",
    "Camp. CPA": "camp_cpa",
    "Camp. tCPA": "camp_tcpa",
    "MTD Cluster Spend": "mtd_cluster_spend",
    "Label budget": "label_budget",
    "Label cost": "label_cost",
    "Label 3D cost": "label_3d_cost",
    "Label conv.": "label_conv",
    "Label remaining budget": "label_remaining_budget",
    "Label KPI value": "label_kpi_value",
    "Label CPA": "label_cpa",
}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def detect_platform(campaign_name: str | None) -> str | None:
    if not campaign_name:
        return None
    s = str(campaign_name).lower()
    if "android" in s:
        return "Android"
    if "ios" in s:
        return "iOS"
    return None


@router.get("/ping")
def ping():
    return {"ok": True}


@router.post("/upload")
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1) Format kontrolü
    if not file.filename or not file.filename.lower().endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Please upload a .xlsx file.")

    # 2) Dosyayı oku
    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    # 3) Excel parse
    try:
        headers, rows = read_excel_bytes(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Excel parse error: {e}")

    # 4) Kolon validasyonu
    missing = validate_required_columns(headers, REQUIRED_COLUMNS)
    if missing:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Missing required columns",
                "missing": missing,
                "found_headers": headers,
            },
        )

    inserted = 0
    updated = 0
    skipped = 0

    for row in rows:
        campaign_name = row.get("Campaign name")
        label = row.get("Labels on Campaign")

        if not campaign_name or not label:
            skipped += 1
            continue

        campaign_name = str(campaign_name).strip()
        label = str(label).strip()
        platform = detect_platform(campaign_name)

        existing = (
            db.query(Record)
            .filter(Record.label == label, Record.campaign_name == campaign_name)
            .first()
        )

        if existing:
            rec = existing
            updated += 1
        else:
            rec = Record(label=label, campaign_name=campaign_name)
            inserted += 1

        rec.platform = platform

        # Excel -> model alanlarını set et
        for excel_col, model_field in EXCEL_TO_MODEL.items():
            val = row.get(excel_col)
            try:
                setattr(rec, model_field, float(val) if val is not None else None)
            except Exception:
                setattr(rec, model_field, None)

        if not existing:
            db.add(rec)

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
    return [f"{r.methods} {r.path}" for r in router.routes]