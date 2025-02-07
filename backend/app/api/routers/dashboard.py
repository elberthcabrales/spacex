from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.usecases.get_dashboard_stats import GetDashboardStatsUseCase
from app.core.domain.dashboard import DashboardStatistics
from app.infrastructure.db.database import get_session
from app.infrastructure.repositories.dashboard_repository import DashboardRepository

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_model=list[DashboardStatistics], summary="Get SpaceX Dashboard Statistics")
def get_dashboard(db: Session = Depends(get_session)):
    """
    🚀 Get SpaceX Dashboard Statistics
    Retrieves key statistics about SpaceX data.

    Returns:
    - List of JSON objects containing all relevant statistics.
    """
    dashboard_repository = DashboardRepository(db)
    use_case = GetDashboardStatsUseCase(dashboard_repository)

    return use_case.execute()