import pytest
from sqlmodel import SQLModel, Session, create_engine

from app.core.domain.rocket import Rocket
from app.core.domain.second_stage import SecondStage

@pytest.fixture
def session():
    """
    Provides an in-memory SQLite session for testing.
    Each test starts with a fresh database schema.
    """
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_create_second_stage(session):
    # 1. Create a rocket first, because second_stage references rocket_uuid
    rocket = Rocket(
        rocket_uuid="second-stage-uuid",
        name="Test Rocket",
        active=True,
    )
    session.add(rocket)
    session.commit()
    session.refresh(rocket)

    # 2. Create a new SecondStage referencing that rocket
    ss = SecondStage(
        reusable=False,
        engines=1,
        fuel_amount_tons=90,
        rocket_uuid="second-stage-uuid",  # same rocket's rocket_uuid
    )
    session.add(ss)
    session.commit()
    session.refresh(ss)

    # 3. Assert the DB assigned an ID and retained correct fields
    assert ss.id is not None
    assert ss.reusable is False
    assert ss.engines == 1
    assert ss.fuel_amount_tons == 90
    assert ss.rocket_uuid == rocket.rocket_uuid
