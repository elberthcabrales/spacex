from sqlalchemy.orm import Session
from sqlalchemy.sql import func, case
from app.core.domain.rocket import Rocket
from app.core.domain.first_stage import FirstStage
from app.core.domain.second_stage import SecondStage
from app.core.domain.launch import Launch
from app.core.domain.failure import Failure
from app.core.domain.starlink import Starlink
from app.core.domain.dashboard import DashboardStatistics

def get_dashboard_statistics(db: Session) -> list[DashboardStatistics]:
    """Fetch SpaceX statistics for the dashboard."""

    query = (
        db.query(
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

    results = query.all()

    return [
        DashboardStatistics(
            rocket_name=row.rocket_name,
            active=row.active,
            first_flight=row.first_flight,
            weight=row.weight,
            height=row.height,
            diameter=row.diameter,
            cost_per_launch=row.cost_per_launch,
            stages=row.stages,
            first_stage_reusable=row.first_stage_reusable,
            first_stage_engines=row.first_stage_engines,
            first_stage_fuel_amount_tons=row.first_stage_fuel_amount_tons,
            second_stage_reusable=row.second_stage_reusable,
            second_stage_engines=row.second_stage_engines,
            second_stage_fuel_amount_tons=row.second_stage_fuel_amount_tons,
            total_successful_launches=row.total_successful_launches,
            total_upcoming_launches=row.total_upcoming_launches,
            total_failures=row.total_failures,
        )
        for row in results
    ]
