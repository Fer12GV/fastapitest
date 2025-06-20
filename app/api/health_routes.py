from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from app.database import engine

router = APIRouter()


@router.get("/health", tags=["Health Check"])
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except SQLAlchemyError as e:
        print(f"[HEALTH ERROR] {e}")
        return {"status": "error", "database": "disconnected"}
