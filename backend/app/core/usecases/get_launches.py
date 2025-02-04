from typing import Optional
from sqlmodel import Session
from app.core.domain.launch import PaginatedLaunchResponse
from app.infrastructure.repositories.launch_repository import LaunchRepository

class GetLaunchesUseCase:
    """
    Use case for retrieving launches with filtering, sorting, and pagination.
    """
    def __init__(self, session: Session):
        self.repository = LaunchRepository(session)

    def execute(
        self,
        details: Optional[str] = None,
        upcoming: Optional[bool] = None,
        success: Optional[bool] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = "asc",
        skip: int = 0,
        limit: int = 10
    ) -> PaginatedLaunchResponse:
        """Retrieve filtered and paginated launches with related data."""
        
        launches, total_count = self.repository.get_all(
            details=details,
            upcoming=upcoming,
            success=success,
            sort_by=sort_by,
            order=order,
            skip=skip,
            limit=limit
        )

        return PaginatedLaunchResponse(
            total=total_count,
            skip=skip,
            limit=limit,
            data=launches
        )
