import pytest
from unittest.mock import patch, MagicMock
from sqlmodel import SQLModel, Session, create_engine

from app.core.domain.rocket import Rocket
from app.infrastructure.scripts.rocket_loader import fetch_and_load_rockets

@pytest.fixture
def session():
    """Provides a temporary in-memory SQLite session for testing."""
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@patch("app.infrastructure.scripts.rocket_loader.requests.get")
def test_fetch_and_load_rockets(mock_get, session):
    # 1. Arrange: mock the API response
    mock_response_data = [
        {
            "id": "spacex-uuid-123",
            "name": "Falcon 9",
            "active": True,
            "stages": 2,
            "cost_per_launch": 50000000,
            "first_flight": "2010-06-04",
            "country": "United States",
            "description": "Rocket used by SpaceX",
            "wikipedia": "https://en.wikipedia.org/wiki/Falcon_9",
            "height": {"meters": 70, "feet": 229.6},
            "diameter": {"meters": 3.7, "feet": 12.1},
            "mass": {"kg": 540000, "lb": 1190000}
        },
    ]
    mock_get.return_value = MagicMock(status_code=200, json=lambda: mock_response_data)

    # 2. Act: call the function that fetches and loads data
    fetch_and_load_rockets(session=session)

    # 3. Assert: check the data in the DB
    rockets_in_db = session.query(Rocket).all()
    assert len(rockets_in_db) == 1
    rocket = rockets_in_db[0]
    assert rocket.rocket_uuid == "spacex-uuid-123"
    assert rocket.name == "Falcon 9"
    assert rocket.active is True
    assert rocket.stages == 2
    assert rocket.country == "United States"
    assert rocket.height == 70.0       # from "height.meters"
    assert rocket.diameter == 3.7      # from "diameter.meters"
    assert rocket.weight == "540000"   # stored as text
