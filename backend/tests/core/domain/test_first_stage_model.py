import pytest
from sqlmodel import SQLModel, Session, create_engine

from app.core.domain.first_stage import FirstStage
from app.core.domain.rocket import Rocket

@pytest.fixture
def session():
    """
    Provides an in-memory SQLite session for testing.
    Each test will start with a fresh database schema.
    """
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_create_first_stage(session):
    # 1. We need a Rocket record first, because first_stage references rocket_uuid
    rocket = Rocket(
        rocket_uuid="abc-123",
        name="Test Rocket",
        active=True,
    )
    session.add(rocket)
    session.commit()
    session.refresh(rocket)

    # 2. Create a new FirstStage referencing that rocket
    fs = FirstStage(
        reusable=True,
        engines=9,
        fuel_amount_tons=385,
        burn_time_sec=162,
        rocket_uuid="abc-123",  # references the rocket created above
    )

    session.add(fs)
    session.commit()
    session.refresh(fs)

    # 3. Assertions
    assert fs.id is not None
    assert fs.reusable is True
    assert fs.engines == 9
    assert fs.fuel_amount_tons == 385
    assert fs.burn_time_sec == 162
    assert fs.rocket_uuid == "abc-123"

    # 4. Confirm we can query it back
    stored_fs = session.get(FirstStage, fs.id)
    assert stored_fs is not None
    assert stored_fs.rocket_uuid == rocket.rocket_uuid
