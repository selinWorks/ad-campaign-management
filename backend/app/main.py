from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import Base, engine
from app.models import record  # noqa: F401 (tablo oluşması için model import)

from app.api.excel import router as excel_router
from app.api.records import router as records_router
from app.api.calculate import router as calculate_router
from app.api.export import router as export_router

app = FastAPI(title="Advanced Internet Programming Final Project")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB tablolarını oluştur
Base.metadata.create_all(bind=engine)

# Router'lar
app.include_router(excel_router)
app.include_router(records_router)
app.include_router(calculate_router)
app.include_router(export_router)

@app.get("/health")
def health():
    return {"ok": True}