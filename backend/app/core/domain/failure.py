from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.core.domain.launch import Launch

class Failure(SQLModel, table=True):
    __tablename__ = "failures"

    id: Optional[int] = Field(default=None, primary_key=True)
    time: Optional[int] = Field(default=None)  # Time of failure in seconds
    reason: Optional[str] = Field(default=None)  # Reason for failure
    launched_uuid: str = Field(
        foreign_key="launches.launched_uuid", nullable=False
    )

    # Many-to-One Relationship with Launch
    launch: Optional["Launch"] = Relationship(back_populates="failures")
