from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
import os

# Database URL (Environment Variable for Security)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:12341234@localhost:5432/spacex")

# Create Engine
engine: Engine = create_engine(DATABASE_URL, echo=True, future=True)

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    """Dependency injection for database session."""
    with SessionLocal() as session:
        yield session


def init_db():
    """Initialize database - Runs only once at startup."""
    from app.core.domain import rocket, first_stage, second_stage, launch, failure, starlink  # Import models
    SQLModel.metadata.create_all(engine)
