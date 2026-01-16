from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Render bazen postgres:// verir. Biz psycopg3 kullanacağız:
# SQLAlchemy'nin psycopg3 kullanması için şema: postgresql+psycopg:// olmalı.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)

# Bazı yerlerde postgresql:// gelir; yine psycopg3'e zorlayalım.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Debug (şifreyi loglamayalım)
_safe_url = DATABASE_URL
if "@" in _safe_url:
    _safe_url = _safe_url.split("@", 1)[0] + "@..."
print("DATABASE_URL(raw) =", _safe_url)
print("DB DIALECT =", DATABASE_URL.split(":", 1)[0])

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=not DATABASE_URL.startswith("sqlite"),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)