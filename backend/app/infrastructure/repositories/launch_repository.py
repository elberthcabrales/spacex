from typing import List, Optional
from sqlalchemy import func, asc, desc
from sqlmodel import select
from sqlalchemy.orm import Session, joinedload
from app.core.domain.launch import Launch
from app.core.domain.rocket import Rocket
from app.core.domain.failure import Failure

class LaunchRepository:
    """
    Repository for retrieving launches with filtering, sorting, and pagination.
    """
    def __init__(self, session: Session):
        self.session = session

    def get_all(
        self,
        mission_name: Optional[str] = None,
        details: Optional[str] = None,
        upcoming: Optional[bool] = None,
        success: Optional[bool] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = "asc",
        skip: int = 0,
        limit: int = 10
    ):
        """Retrieve all launches with filters, sorting, and pagination."""

        query = (
            select(Launch)
            .options(
                joinedload(Launch.rocket), 
                joinedload(Launch.failures)
            )
        )

        # Apply filters
        filters = []
        if mission_name:
            filters.append(Launch.mission_name.ilike(f"%{mission_name}%"))
        if details:
            filters.append(Launch.details.ilike(f"%{details}%"))
        if upcoming is not None:
            filters.append(Launch.upcoming == upcoming)
        if success is not None:
            filters.append(Launch.success == success)

        if filters:
            query = query.where(*filters)

        # Sorting options with proper joins
        sort_options = {
            "mission_name": Launch.mission_name,
            "details": Launch.details,
            "success": Launch.success,
            "upcoming": Launch.upcoming,
            "rocket_name": Rocket.name,
            "rocket_cost": Rocket.cost_per_launch,
            "rocket_active": Rocket.active,
            "failures": Failure.reason,  # Sorting by failure reason
        }

        # Validate `sort_by` to avoid KeyError
        if sort_by and sort_by in sort_options:
            sort_field = sort_options[sort_by]
            
            # If sorting by a related table (Rocket, Failure), we need to join it
            if sort_by in ["rocket_name", "rocket_cost", "rocket_active"]:
                query = query.join(Rocket, Launch.rocket_uuid == Rocket.rocket_uuid)
            elif sort_by == "failures":
                query = query.outerjoin(Failure, Launch.launched_uuid == Failure.launched_uuid)
            
            # Apply sorting order
            query = query.order_by(desc(sort_field) if order == "desc" else asc(sort_field))

        # Get total count before pagination
        total_count = self.session.execute(select(func.count()).select_from(query.subquery())).scalar_one()

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query and ensure unique results
        results = self.session.execute(query).scalars().unique().all()

        # Format response
        launches = [
            {
                "mission_name": launch.mission_name,
                "details": launch.details,
                "upcoming": launch.upcoming,
                "success": launch.success,
                "image": launch.image,
                "webcast": launch.webcast,
                "article": launch.article,
                "rocket": {
                    "rocket_uuid": launch.rocket.rocket_uuid if launch.rocket else None,
                    "name": launch.rocket.name if launch.rocket else None,
                    "cost_per_launch": launch.rocket.cost_per_launch if launch.rocket else None,
                    "active": launch.rocket.active if launch.rocket else None
                },
                "failures": [{"time": f.time, "reason": f.reason} for f in launch.failures],
            }
            for launch in results
        ]

        return launches, total_count
