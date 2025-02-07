from typing import List, Optional
from sqlalchemy import func
from sqlmodel import select
from sqlalchemy.orm import Session, joinedload
from app.core.domain.starlink import Starlink
from app.core.domain.launch import Launch
from app.core.domain.rocket import Rocket

class StarlinkRepository:
    """
    Repository for retrieving Starlinks with filtering, sorting, and pagination.
    """
    def __init__(self, session: Session):
        self.session = session

    def get_all(
        self,
        name: Optional[str] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = "asc",
        skip: int = 0,
        limit: int = 10
    ):
        """Retrieve all Starlinks with filters, sorting, and pagination."""

        query = (
            select(Starlink)
            .options(
                joinedload(Starlink.launch).joinedload(Launch.rocket)  # Include Launch & Rocket
            )
        )

        # Apply filters
        filters = []
        if name:
            filters.append(Starlink.name.ilike(f"%{name}%"))

        if filters:
            query = query.where(*filters)

        # Sorting options
        sort_options = {
            "name": Starlink.name,
            "creation_date": Starlink.creation_date,
        }
        sort_field = sort_options.get(sort_by, Starlink.id)  # Default sorting by ID
        query = query.order_by(sort_field.desc() if order == "desc" else sort_field.asc())

        # Get total count before pagination
        total_count = self.session.execute(select(func.count()).select_from(query.subquery())).scalar_one()

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query with unique results
        results = self.session.execute(query).unique().scalars().all()

        # Format response
        starlinks = [
            {
                "starlink_uuid": starlink.starlink_uuid,
                "name": starlink.name,
                "creation_date": starlink.creation_date,
                "rocket": {
                    "name": starlink.launch.rocket.name if starlink.launch and starlink.launch.rocket else None,
                    "cost_per_launch": starlink.launch.rocket.cost_per_launch if starlink.launch and starlink.launch.rocket else None,
                    "first_flight": starlink.launch.rocket.first_flight if starlink.launch and starlink.launch.rocket else None,

                } if starlink.launch else None
            }
            for starlink in results
        ]

        print("Starlinks found:", len(starlinks))

        return starlinks, total_count
