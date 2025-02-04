from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from app.infrastructure.db.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.get("/health", tags=["health"])
def health_check(session: Session = Depends(get_session)):
    """Health check to verify database connectivity."""
    try:
        session.execute("SELECT 1")
        return {"status": "healthy"}
    except SQLAlchemyError:
        return {"status": "unhealthy"}
