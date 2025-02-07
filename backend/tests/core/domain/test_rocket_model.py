import pytest
from sqlmodel import SQLModel, Session, create_engine
from app.core.domain.rocket import Rocket

@pytest.fixture
def session():
    # In-memory SQLite for quick tests
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_create_rocket(session):
    # 1. Arrange
    new_rocket = Rocket(
        rocket_uuid="unique-uuid-123",
        description="Test Rocket Description",
        name="Falcon 9",
        active=True,
        wikipedia="https://en.wikipedia.org/wiki/Falcon_9",
        weight=540,
        height=70.0,
        diameter=3.7,
        cost_per_launch=50000000,
        first_flight="2010-06-04",
        country="United States",
        stages=2
    )

    # 2. Act
    session.add(new_rocket)
    session.commit()
    session.refresh(new_rocket)

    # 3. Assert
    assert new_rocket.id is not None
    assert new_rocket.rocket_uuid == "unique-uuid-123"
    assert new_rocket.name == "Falcon 9"
    assert new_rocket.active is True
    assert new_rocket.cost_per_launch == 50000000
    assert new_rocket.stages == 2
