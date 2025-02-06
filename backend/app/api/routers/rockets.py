from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from enum import Enum
from sqlmodel import Session
from app.infrastructure.db.database import get_session
from app.core.usecases.get_rockets import GetRocketsUseCase
from app.core.domain.rocket import RocketResponse, PaginatedRocketResponse, RocketQueryParams

router = APIRouter()

class SortOptions(str, Enum):
    name = "name"
    height = "height"
    diameter = "diameter"
    country = "country"
    cost_per_launch = "cost_per_launch"
    first_flight="first_flight"
    
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
    rocket_uuid: Optional[str] = Query(None, description="Filter by rocket UUID"),
    sort_by: Optional[SortOptions] = Query(None, description="Sort by height, diameter, or cost_per_launch"),
    order: Optional[str] = Query("asc", description="Sorting order: asc (ascending) or desc (descending)"),
    session: Session = Depends(get_session)
):
    """API endpoint to list rockets with pagination, filtering, and sorting."""
       # Ensure query parameters are properly formatted
    name = name.strip() if name else None
    use_case = GetRocketsUseCase(session)
    
    return use_case.execute(
        name=name,
        rocket_uuid=rocket_uuid,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit
    )