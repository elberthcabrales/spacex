from fastapi import APIRouter, Depends, Query
from typing import Optional
from enum import Enum
from sqlalchemy.orm import Session
from sqlmodel import Field
from app.infrastructure.db.database import get_session
from app.core.usecases.get_starlinks import GetStarlinksUseCase
from app.core.domain.starlink import PaginatedStarlinkResponse

router = APIRouter()

class SortOptions(str, Enum):
    name: Optional[str] = Field(default=None, title="Starlink Name", description="The name of the rocket")
    creation_date: Optional[str] = Field(default=None)  # spaceTrack.creation_date
    object_name: Optional[str] = Field(default=None)  # spaceTrack.object_name
    country_code: Optional[str] = Field(default=None)  # spaceTrack.country_code


@router.get(
    "/starlinks/",
    response_model=PaginatedStarlinkResponse,
    summary="Get all Starlinks with pagination and filters",
    description="Retrieve a list of all Starlinks with optional filtering by name, object name, country, and pagination support.",
    tags=["Starlinks"]
)

def list_starlinks(
    name: Optional[str] = Query(None, description="Filter by Starlink name"),
    sort_by: Optional[SortOptions] = Query(None, description="Sort by name, creation_date, or object_name"),
    order: Optional[str] = Query("asc", description="Sorting order: asc (ascending) or desc (descending)"),
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(10, description="Number of records to return for pagination"),
    session: Session = Depends(get_session)
):
    """API endpoint to list Starlinks with pagination and filtering."""
    use_case = GetStarlinksUseCase(session)
    return use_case.execute(
        name=name,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit
    )
