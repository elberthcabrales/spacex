from sqlalchemy.orm import Session
from sqlalchemy.sql import func, case
from app.core.domain.rocket import Rocket
from app.core.domain.first_stage import FirstStage
from app.core.domain.second_stage import SecondStage
from app.core.domain.launch import Launch
from app.core.domain.failure import Failure

class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_statistics(self):
        """Fetch SpaceX statistics for the dashboard."""
        query = (
            self.db.query(
                Rocket.name.label("rocket_name"),
                Rocket.active,
                Rocket.first_flight,
                Rocket.weight,
                Rocket.height,
                Rocket.diameter,
                Rocket.cost_per_launch,
                Rocket.stages,
                FirstStage.reusable.label("first_stage_reusable"),
                FirstStage.engines.label("first_stage_engines"),
                FirstStage.fuel_amount_tons.label("first_stage_fuel_amount_tons"),
                SecondStage.reusable.label("second_stage_reusable"),
                SecondStage.engines.label("second_stage_engines"),
                SecondStage.fuel_amount_tons.label("second_stage_fuel_amount_tons"),
                func.count(case((Launch.success == True, 1))).label("total_successful_launches"),
                func.count(case((Launch.upcoming == True, 1))).label("total_upcoming_launches"),
                func.count(Failure.id).label("total_failures"),
            )
            .outerjoin(FirstStage, Rocket.rocket_uuid == FirstStage.rocket_uuid)
            .outerjoin(SecondStage, Rocket.rocket_uuid == SecondStage.rocket_uuid)
            .outerjoin(Launch, Rocket.rocket_uuid == Launch.rocket_uuid)
            .outerjoin(Failure, Launch.launched_uuid == Failure.launched_uuid)
            .group_by(
                Rocket.name,
                Rocket.active,
                Rocket.first_flight,
                Rocket.weight,
                Rocket.height,
                Rocket.diameter,
                Rocket.cost_per_launch,
                Rocket.stages,
                FirstStage.reusable,
                FirstStage.engines,
                FirstStage.fuel_amount_tons,
                SecondStage.reusable,
                SecondStage.engines,
                SecondStage.fuel_amount_tons
            )
        )
        return query.all()