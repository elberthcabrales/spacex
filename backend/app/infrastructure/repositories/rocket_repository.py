from typing import Optional
from sqlalchemy import func
from sqlmodel import select
from sqlalchemy.orm import Session
from app.core.domain.rocket import Rocket

class RocketRepository:
    """Repository for retrieving rockets with filtering, sorting, and pagination."""

    def __init__(self, session: Session):
        self.session = session

    def get_all(
        self,
        name: Optional[str] = None,
        rocket_uuid: Optional[str] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = "asc",
        skip: int = 0,
        limit: int = 10
    ):
        """Retrieve all rockets with filters, sorting, and pagination."""
        
        query = select(Rocket)

        # Apply filters
        filters = []
        if rocket_uuid:
            filters.append(Rocket.rocket_uuid == rocket_uuid)
        elif name:
            filters.append(Rocket.name.ilike(f"%{name}%"))

        # Apply all filters at once
        if filters:
            query = query.where(*filters)

        # Apply sorting
        sort_options = {
            "name": Rocket.name,
            "height": Rocket.height,
            "country": Rocket.country,
            "diameter": Rocket.diameter,
            "cost_per_launch": Rocket.cost_per_launch,
            "first_flight": Rocket.first_flight
        }
        sort_field = sort_options.get(sort_by, Rocket.name)  # Default sorting by ID

        if order == "desc":
            query = query.order_by(sort_field.desc())
        else:
            query = query.order_by(sort_field.asc())

        # Debugging: Print the final SQL query for troubleshooting
        print(str(query))

        # Get total count before pagination
        total_count = self.session.execute(select(func.count()).select_from(query.subquery())).scalar_one()

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute the final query
        rockets = self.session.execute(query).scalars().all()

        return rockets, total_count
