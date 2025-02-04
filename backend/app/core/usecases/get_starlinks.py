from typing import Optional
from sqlmodel import Session
from app.core.domain.starlink import PaginatedStarlinkResponse
from app.infrastructure.repositories.starlink_repository import StarlinkRepository

class GetStarlinksUseCase:
    """
    Use case for retrieving Starlinks with filtering, sorting, and pagination.
    """
    def __init__(self, session: Session):
        self.repository = StarlinkRepository(session)

    def execute(
        self,
        name: Optional[str] = None,
        object_name: Optional[str] = None,
        country_code: Optional[str] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = "asc",
        skip: int = 0,
        limit: int = 10
    ) -> PaginatedStarlinkResponse:
        """Retrieve filtered and paginated Starlinks."""

        starlinks, total_count = self.repository.get_all(
            name=name,
            object_name=object_name,
            country_code=country_code,
            sort_by=sort_by,
            order=order,
            skip=skip,
            limit=limit
        )

        return PaginatedStarlinkResponse(
            total=total_count,
            skip=skip,
            limit=limit,
            data=starlinks
        )
