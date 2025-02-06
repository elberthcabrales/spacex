from sqlmodel import SQLModel, Field, Relationship
from app.core.domain.launch import Launch
from typing import List, Optional

class Starlink(SQLModel, table=True):
    __tablename__ = "starlinks"

    id: Optional[int] = Field(default=None, primary_key=True)
    starlink_uuid: str = Field(unique=True, nullable=False)  # ID from SpaceX API
    name: Optional[str] = Field(default=None)
    creation_date: Optional[str] = Field(default=None)  # spaceTrack.creation_date
    country_code: Optional[str] = Field(default=None)  # spaceTrack.country_code
    object_name: Optional[str] = Field(default=None)  # spaceTrack.object_name
    launched_uuid: Optional[str] = Field(
        foreign_key="launches.launched_uuid", nullable=True
    )

    # Many-to-One Relationship with Launch (optional)
    launch: Optional["Launch"] = Relationship(back_populates="starlinks")



class StarlinkBase(SQLModel):
    """
    Base schema for Starlink containing shared attributes.
    """
    starlink_uuid: str = Field(unique=True, nullable=False, title="Starlink UUID", description="Unique identifier for the Starlink")
    name: Optional[str] = Field(default=None, title="Name", description="Name of the Starlink satellite")
    creation_date: Optional[str] = Field(default=None, title="Creation Date", description="Date when the satellite was created")
    country_code: Optional[str] = Field(default=None, title="Country Code", description="Country code of origin")

class StarlinkResponse(StarlinkBase):
    """
    API response schema for Starlinks.
    """
    rocket: Optional[dict] = Field(default=None, title="Rocket", description="Rocket details related to the launch")

class PaginatedStarlinkResponse(SQLModel):
    """
    Paginated response schema for Starlinks.
    """
    total: int = Field(title="Total Records", description="Total number of Starlinks matching the query")
    skip: int = Field(title="Skipped Records", description="Number of records skipped")
    limit: int = Field(title="Returned Records", description="Number of records returned")
    data: List[StarlinkResponse] = Field(title="Starlink Data", description="List of Starlinks matching the query")
