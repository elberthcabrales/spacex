import pytest
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text  # Import text for raw SQL queries
from app.infrastructure.db.database import get_session

def test_database_connection():
    """Ensure the database connection is working."""
    try:
        with next(get_session()) as session:
            session.execute(text("SELECT 1"))  # Explicitly declare text
    except OperationalError:
        pytest.fail("Database connection failed")
