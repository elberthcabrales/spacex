from typing import Optional

from sqlmodel import Session
from app.core.domain.rocket import PaginatedRocketResponse
from app.infrastructure.repositories.rocket_repository import RocketRepository


class GetRocketsUseCase:
    """Use case for retrieving rockets with filtering, sorting, and pagination."""

    def __init__(self, session: Session):
        self.repository = RocketRepository(session)

    def execute(
        self,
        name: Optional[str] = None,
        rocket_uuid: Optional[str] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = "asc",
        skip: int = 0,
        limit: int = 10
    ) -> PaginatedRocketResponse:
        """Retrieve filtered and paginated rockets."""

        rockets, total_count = self.repository.get_all(
            name=name,
            rocket_uuid=rocket_uuid,
            sort_by=sort_by,
            order=order,
            skip=skip,
            limit=limit
        )

        return PaginatedRocketResponse(
            total=total_count,
            skip=skip,
            limit=limit,
            data=rockets
        )
