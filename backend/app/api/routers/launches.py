from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.infrastructure.db.database import get_session
from app.core.usecases.get_launches import GetLaunchesUseCase
from app.core.domain.launch import PaginatedLaunchResponse

router = APIRouter()

@router.get(
    "/launches/",
    response_model=PaginatedLaunchResponse,
    summary="Get all launches with pagination and filters",
    description="Retrieve a list of launches with optional filtering, sorting, and pagination.",
    tags=["Launches"]
)
def list_launches(
    details: Optional[str] = Query(None, description="Filter by launch details"),
    upcoming: Optional[bool] = Query(None, description="Filter by upcoming launches"),
    success: Optional[bool] = Query(None, description="Filter by successful launches"),
    sort_by: Optional[str] = Query(None, description="Sort by success, upcoming, or article"),
    order: Optional[str] = Query("asc", description="Sorting order: asc (ascending) or desc (descending)"),
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(10, description="Number of records to return for pagination"),
    session: Session = Depends(get_session)
):
    """API endpoint to list launches with pagination and filtering."""
    use_case = GetLaunchesUseCase(session)
    return use_case.execute(
        details=details,
        upcoming=upcoming,
        success=success,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit
    )
