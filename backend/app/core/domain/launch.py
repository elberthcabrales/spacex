from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from app.core.domain.rocket import RocketResponse
class Launch(SQLModel, table=True):
    __tablename__ = "launches"

    id: Optional[int] = Field(default=None, primary_key=True)
    launched_uuid: str = Field(unique=True, nullable=False)
    mission_name: Optional[str] = Field(default=None)
    details: Optional[str] = Field(default=None)
    upcoming: Optional[bool] = Field(default=None)
    success: Optional[bool] = Field(default=None)
    image: Optional[str] = Field(default=None)  # links.patch.small
    webcast: Optional[str] = Field(default=None)  # links.webcast
    article: Optional[str] = Field(default=None)
    rocket_uuid: Optional[str] = Field(
        foreign_key="rockets.rocket_uuid", nullable=True
    )

    # One-to-One Relationship with Rocket
    rocket: Optional["Rocket"] = Relationship(back_populates="launches")

    failures: list["Failure"] = Relationship(back_populates="launch")

    starlinks: List["Starlink"] = Relationship(back_populates="launch")

class FailureResponse(SQLModel):
    """API response schema for a Failure event."""
    time: Optional[int] = Field(default=None, title="Time", description="Time of failure in seconds")
    reason: Optional[str] = Field(default=None, title="Reason", description="Reason for failure")

class StarlinkResponse(SQLModel):
    """API response schema for a Starlink event."""
    starlink_uuid: str = Field(title="Starlink UUID", description="Unique identifier for the Starlink satellite")
    name: Optional[str] = Field(default=None, title="Name", description="Name of the Starlink satellite")

class RocketResponse(SQLModel):
    name: str
    cost_per_launch: int
    active: bool
    
class LaunchResponse(SQLModel):
    """API response schema for Launches."""
    launched_uuid: str = Field(title="Launch UUID", description="Unique identifier for the launch")
    mission_name: Optional[str] = Field(default=None, title="Mission Name", description="Name of the mission")
    details: Optional[str] = Field(default=None, title="Details", description="Description of the launch")
    upcoming: Optional[bool] = Field(default=None, title="Upcoming", description="Whether the launch is upcoming")
    success: Optional[bool] = Field(default=None, title="Success", description="Whether the launch was successful")
    image: Optional[str] = Field(default=None, title="Image", description="URL to the launch image")
    webcast: Optional[str] = Field(default=None, title="Webcast", description="URL to the webcast of the launch")
    article: Optional[str] = Field(default=None, title="Article", description="URL to an article about the launch")

    # Related data
    rocket: Optional[RocketResponse] = Field(default=None, title="Rocket", description="Rocket details")
    failures: List[FailureResponse] = Field(default=[], title="Failures", description="List of failures related to the launch")

class PaginatedLaunchResponse(SQLModel):
    """Paginated response schema for launches."""
    total: int = Field(title="Total Records", description="Total number of launches matching the query")
    skip: int = Field(title="Skipped Records", description="Number of records skipped")
    limit: int = Field(title="Returned Records", description="Number of records returned")
    data: List[LaunchResponse] = Field(title="Launch Data", description="List of launches matching the query")

