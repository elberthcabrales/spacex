from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Launch(SQLModel, table=True):
    __tablename__ = "launches"

    id: Optional[int] = Field(default=None, primary_key=True)
    launched_uuid: str = Field(unique=True, nullable=False)
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
