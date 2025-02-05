from pydantic import BaseModel
from typing import Optional

class LatestLaunch(BaseModel):
    """Model representing the latest SpaceX launch details."""
    mission_name: Optional[str]
    launch_date: Optional[str]
    success: Optional[bool]

class DashboardStatistics(BaseModel):
    """Model representing SpaceX statistics for the dashboard."""
    total_launches: int
    successful_launches: int
    failed_launches: int
    total_rockets: int
    total_starlinks: int
    latest_launch: Optional[LatestLaunch]
