from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.core.domain.launch import Launch

class Starlink(SQLModel, table=True):
    __tablename__ = "starlinks"

    id: Optional[int] = Field(default=None, primary_key=True)
    starlink_uuid: str = Field(unique=True, nullable=False)  # ID from SpaceX API
    name: Optional[str] = Field(default=None)
    creation_date: Optional[str] = Field(default=None)  # spaceTrack.creation_date
    object_name: Optional[str] = Field(default=None)  # spaceTrack.object_name
    country_code: Optional[str] = Field(default=None)  # spaceTrack.country_code
    launched_uuid: Optional[str] = Field(
        foreign_key="launches.launched_uuid", nullable=True
    )

    # Many-to-One Relationship with Launch (optional)
    launch: Optional["Launch"] = Relationship(back_populates="starlinks")
