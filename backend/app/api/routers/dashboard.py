from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.usecases.get_dashboard_stats import get_dashboard_statistics
from app.core.domain.dashboard import DashboardStatistics
from app.infrastructure.db.database import get_session

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_model=list[DashboardStatistics], summary="Get SpaceX Dashboard Statistics")
def get_dashboard(session: Session = Depends(get_session)):
    """
    🚀 Get SpaceX Dashboard Statistics
    Retrieves key statistics about SpaceX data.

    Returns:
    - List of JSON objects containing all relevant statistics.
    """
    return get_dashboard_statistics(session)
