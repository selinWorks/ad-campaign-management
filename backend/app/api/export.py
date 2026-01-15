from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.record import Record
from app.services.export.excel_export import records_to_excel

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/ping")
def ping():
    return {"ok": True}


@router.get("/excel")
def export_excel(db: Session = Depends(get_db)):
    records = db.query(Record).all()
    if not records:
        raise HTTPException(status_code=404, detail="No records to export")

    excel_file = records_to_excel(records)

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=calculated_results.xlsx"
        },
    )