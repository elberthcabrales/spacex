from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.core.domain.first_stage import FirstStage
from app.core.domain.second_stage import SecondStage

class RocketBase(SQLModel):
    """
    Base schema for Rocket containing shared attributes.
    Used for request and response models.
    """
    name: Optional[str] = Field(default=None, title="Rocket Name", description="The name of the rocket")
    active: Optional[bool] = Field(default=None, title="Active", description="Is the rocket still in service?")
    wikipedia: Optional[str] = Field(default=None, title="Wikipedia Link", description="Link to Wikipedia page")
    weight: Optional[str] = Field(default=None, title="Weight", description="Weight in kg")
    height: Optional[float] = Field(default=None, title="Height", description="Height in meters")
    diameter: Optional[float] = Field(default=None, title="Diameter", description="Diameter in meters")
    cost_per_launch: Optional[int] = Field(default=None, title="Cost Per Launch", description="Launch cost in USD")
    first_flight: Optional[str] = Field(default=None, title="First Flight", description="Date of first flight")
    country: Optional[str] = Field(default=None, title="Country", description="Country of origin")
    stages: Optional[int] = Field(default=None, title="Stages", description="Number of rocket stages")

class Rocket(RocketBase, table=True):
    """
    Database model for Rockets.
    Represents a rocket with its specifications and launch history.
    """
    __tablename__ = "rockets"

    id: Optional[int] = Field(default=None, primary_key=True, title="ID", description="Primary key of the rocket")
    rocket_uuid: str = Field(unique=True, nullable=False, title="Rocket UUID", description="Unique identifier for the rocket")

    # One-to-One Relationships
    first_stage: Optional[FirstStage] = Relationship(
        back_populates="rocket", sa_relationship_kwargs={"uselist": False}
    )
    second_stage: Optional[SecondStage] = Relationship(
        back_populates="rocket", sa_relationship_kwargs={"uselist": False}
    )

    launches: List["Launch"] = Relationship(back_populates="rocket")

class RocketResponse(RocketBase):
    """
    API response schema for Rockets.
    Includes pagination metadata.
    """
    rocket_uuid: str = Field(title="Rocket UUID", description="Unique identifier for the rocket")

class RocketQueryParams(SQLModel):
    """
    Query parameters for filtering, sorting, and paginating rockets.
    """
    name: Optional[str] = Field(default=None, title="Rocket Name", description="Filter by rocket name")
    active: Optional[bool] = Field(default=None, title="Active", description="Filter by active status")
    wikipedia: Optional[bool] = Field(default=None, title="Has Wikipedia", description="Filter by presence of Wikipedia link")
    first_flight: Optional[str] = Field(default=None, title="First Flight Date", description="Filter by first flight date")
    
    sort_by: Optional[str] = Field(default=None, title="Sort By", description="Sort results by height, diameter, or cost_per_launch")
    order: Optional[str] = Field(default="asc", title="Order", description="Sorting order: asc (ascending) or desc (descending)")
    
    skip: int = Field(default=0, title="Skip", description="Number of records to skip for pagination")
    limit: int = Field(default=10, title="Limit", description="Number of records to return for pagination")
    
class PaginatedRocketResponse(SQLModel):
    """
    Paginated response schema for rockets.
    """
    total: int = Field(title="Total Records", description="Total number of rockets matching the query")
    skip: int = Field(title="Skipped Records", description="Number of records skipped")
    limit: int = Field(title="Returned Records", description="Number of records returned")
    data: List[RocketResponse] = Field(title="Rocket Data", description="List of rockets matching the query")
