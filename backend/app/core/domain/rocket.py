# app/core/domain/rocket.py
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.core.domain.first_stage import FirstStage
from app.core.domain.second_stage import SecondStage

class Rocket(SQLModel, table=True):
    __tablename__ = "rockets"

    id: Optional[int] = Field(default=None, primary_key=True)
    rocket_uuid: str = Field(unique=True, nullable=False)
    name: Optional[str] = Field(default=None)
    active: Optional[bool] = Field(default=None)
    wikipedia: Optional[str] = Field(default=None)
    weight: Optional[str] = Field(default=None)
    height: Optional[float] = Field(default=None)
    diameter: Optional[float] = Field(default=None)
    cost_per_launch: Optional[int] = Field(default=None)
    first_flight: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    stages: Optional[int] = Field(default=None)

    # One-to-One Relationships
    first_stage: Optional["FirstStage"] = Relationship(
        back_populates="rocket", sa_relationship_kwargs={"uselist": False}
    )
    second_stage: Optional["SecondStage"] = Relationship(
        back_populates="rocket", sa_relationship_kwargs={"uselist": False}
    )
