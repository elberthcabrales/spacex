from typing import List
from app.core.domain.dashboard import DashboardStatistics
from app.infrastructure.repositories.dashboard_repository import DashboardRepository

class GetDashboardStatsUseCase:
    def __init__(self, dashboard_repository: DashboardRepository):
        self.dashboard_repository = dashboard_repository

    def execute(self) -> List[DashboardStatistics]:
        """Fetch and return SpaceX statistics for the dashboard."""
        results = self.dashboard_repository.get_dashboard_statistics()
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