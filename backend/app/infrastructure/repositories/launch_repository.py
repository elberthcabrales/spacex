from typing import List, Optional
from sqlalchemy import func
from sqlmodel import select
from sqlalchemy.orm import Session, joinedload
from app.core.domain.launch import Launch
from app.core.domain.rocket import Rocket
from app.core.domain.failure import Failure
from app.core.domain.starlink import Starlink

class LaunchRepository:
    """
    Repository for retrieving launches with filtering, sorting, and pagination.
    """
    def __init__(self, session: Session):
        self.session = session

    def get_all(
        self,
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
                joinedload(Launch.failures), 
            )
        )

        # Apply filters
        filters = []
        if details:
            filters.append(Launch.details.ilike(f"%{details}%"))
        if upcoming is not None:
            filters.append(Launch.upcoming == upcoming)
        if success is not None:
            filters.append(Launch.success == success)

        if filters:
            query = query.where(*filters)

        # Sorting
        sort_options = {
            "success": Launch.success,
            "upcoming": Launch.upcoming,
            "article": Launch.article
        }
        sort_field = sort_options.get(sort_by, Launch.id)  # Default sorting by ID
        query = query.order_by(sort_field.desc() if order == "desc" else sort_field.asc())

        # Get total count before pagination
        total_count = self.session.execute(select(func.count()).select_from(query.subquery())).scalar_one()

        # Apply pagination
        query = query.offset(skip).limit(limit)
        print(query)

        # Execute query and ensure unique results
        results = self.session.execute(query).unique().scalars().all()  # ✅ Added `.unique()`

        # Format response
        launches = [
            {
                "launched_uuid": launch.launched_uuid,
                "details": launch.details,
                "upcoming": launch.upcoming,
                "success": launch.success,
                "image": launch.image,
                "webcast": launch.webcast,
                "article": launch.article,
                "rocket": {
                    "name": launch.rocket.name if launch.rocket else None,
                    "cost_per_launch": launch.rocket.cost_per_launch if launch.rocket else None,
                    "active": launch.rocket.active if launch.rocket else None
                },
                "failures": [{"time": f.time, "reason": f.reason} for f in launch.failures],
            }
            for launch in results
        ]

        return launches, total_count
