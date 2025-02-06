from fastapi import APIRouter, Depends, Query
from typing import Optional
from enum import Enum
from sqlalchemy.orm import Session
from app.infrastructure.db.database import get_session
from app.core.usecases.get_launches import GetLaunchesUseCase
from app.core.domain.launch import PaginatedLaunchResponse

router = APIRouter()
class SortOptions(str, Enum):
    mission_name = "mission_name"
    details = "details"
    success = "success"
    upcoming = "upcoming"
    rocket_name = "rocket_name"
    rocket_cost = "rocket_cost"
    rocket_active = "rocket_active"
    failures = "failures"
@router.get(
    "/launches/",
    response_model=PaginatedLaunchResponse,
    summary="Get all launches with pagination and filters",
    description="Retrieve a list of launches with optional filtering, sorting, and pagination.",
    tags=["Launches"]
)
def list_launches(
    details: Optional[str] = Query(None, description="Filter by launch details"),
    mission_name: Optional[str] = Query(None, description="Filter by mission name"),
    sort_by: Optional[SortOptions] = Query(
        None,
        description="Sort by one of the following: mission_name, details, success, upcoming, rocket, rocket_cost, rocket_active, failures"
    ),
    order: Optional[str] = Query("asc", description="Sorting order: asc (ascending) or desc (descending)"),
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(10, description="Number of records to return for pagination"),
    session: Session = Depends(get_session)
):
    """API endpoint to list launches with pagination and filtering."""
    use_case = GetLaunchesUseCase(session)
    return use_case.execute(
        mission_name=mission_name,
        details=details,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit
    )
