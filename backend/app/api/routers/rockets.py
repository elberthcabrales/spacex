from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlmodel import Session
from app.infrastructure.db.database import get_session
from app.core.usecases.get_rockets import GetRocketsUseCase
from app.core.domain.rocket import RocketResponse, PaginatedRocketResponse, RocketQueryParams

router = APIRouter()

@router.get(
    "/rockets/",
    response_model=PaginatedRocketResponse,
    summary="Get a list of rockets",
    tags=["Rockets"]
)
def list_rockets(
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(10, description="Number of records to return for pagination"),
    name: Optional[str] = Query(None, description="Filter by rocket name"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: Optional[str] = Query(None, description="Sort by height, diameter, or cost_per_launch"),
    order: Optional[str] = Query("asc", description="Sorting order: asc (ascending) or desc (descending)"),
    session: Session = Depends(get_session)
):
    """API endpoint to list rockets with pagination, filtering, and sorting."""
       # Ensure query parameters are properly formatted
    name = name.strip() if name else None
    use_case = GetRocketsUseCase(session)
    
    return use_case.execute(
        name=name,
        active=active,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit
    )