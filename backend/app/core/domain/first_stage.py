# app/core/domain/first_stage.py
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class FirstStage(SQLModel, table=True):
    __tablename__ = "first_stage"

    id: Optional[int] = Field(default=None, primary_key=True)
    reusable: Optional[bool] = Field(default=None)
    engines: Optional[int] = Field(default=None)
    fuel_amount_tons: Optional[int] = Field(default=None)
    burn_time_sec: Optional[int] = Field(default=None)
    rocket_uuid: str = Field(
        foreign_key="rockets.rocket_uuid", unique=True, nullable=False
    )

    # One-to-One Relationship
    rocket: Optional["Rocket"] = Relationship(back_populates="first_stage")
