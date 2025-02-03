# app/core/domain/second_stage.py
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class SecondStage(SQLModel, table=True):
    __tablename__ = "second_stage"

    id: Optional[int] = Field(default=None, primary_key=True)
    reusable: Optional[bool] = Field(default=None)
    engines: Optional[int] = Field(default=None)
    fuel_amount_tons: Optional[int] = Field(default=None)
    rocket_uuid: str = Field(
        foreign_key="rockets.rocket_uuid", unique=True, nullable=False
    )

    # One-to-One Relationship
    rocket: Optional["Rocket"] = Relationship(back_populates="second_stage")
