from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.infrastructure.db.database import get_session
from app.core.usecases.get_starlinks import GetStarlinksUseCase
from app.core.domain.starlink import PaginatedStarlinkResponse

router = APIRouter()

@router.get(
    "/starlinks/",
    response_model=PaginatedStarlinkResponse,
    summary="Get all Starlinks with pagination and filters",
    description="Retrieve a list of all Starlinks with optional filtering by name, object name, country, and pagination support.",
    tags=["Starlinks"]
)
def list_starlinks(
    name: Optional[str] = Query(None, description="Filter by Starlink name"),
    object_name: Optional[str] = Query(None, description="Filter by object name"),
    country_code: Optional[str] = Query(None, description="Filter by country code"),
    sort_by: Optional[str] = Query(None, description="Sort by name, creation_date, or object_name"),
    order: Optional[str] = Query("asc", description="Sorting order: asc (ascending) or desc (descending)"),
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(10, description="Number of records to return for pagination"),
    session: Session = Depends(get_session)
):
    """API endpoint to list Starlinks with pagination and filtering."""
    use_case = GetStarlinksUseCase(session)
    return use_case.execute(
        name=name,
        object_name=object_name,
        country_code=country_code,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit
    )
