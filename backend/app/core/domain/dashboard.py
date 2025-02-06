from pydantic import BaseModel
from typing import Optional

class DashboardStatistics(BaseModel):
    rocket_name: str
    active: bool
    first_flight: str
    weight: str
    height: float
    diameter: float
    cost_per_launch: int
    stages: int
    first_stage_reusable: Optional[bool]
    first_stage_engines: Optional[int]
    first_stage_fuel_amount_tons: Optional[int]
    second_stage_reusable: Optional[bool]
    second_stage_engines: Optional[int]
    second_stage_fuel_amount_tons: Optional[int]
    total_successful_launches: int
    total_upcoming_launches: int
    total_failures: int
    total_starlinks_deployed: int
