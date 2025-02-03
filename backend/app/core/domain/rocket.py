from typing import Optional
from sqlmodel import SQLModel, Field

class Rocket(SQLModel, table=True):
    __tablename__ = "rockets"  # Not strictly required; SQLModel infers from class name

    id: Optional[int] = Field(default=None, primary_key=True)
    rocket_uuid: str = Field(unique=True)
    description: Optional[str] = Field(default=None)
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
