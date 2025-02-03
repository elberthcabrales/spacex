import pytest
from app.core.domain.rocket import Rocket

def test_rocket_initialization():
    rocket = Rocket(name="Falcon 9", is_active=True, cost_per_launch=50000000, stages=2)
    assert rocket.name == "Falcon 9"
    assert rocket.is_active is True
    assert rocket.cost_per_launch == 50000000
    assert rocket.stages == 2

def test_rocket_can_reuse():
    rocket = Rocket(name="Falcon 9", is_active=True, cost_per_launch=50000000, stages=2)
    assert rocket.can_reuse() is True

def test_inactive_rocket_cannot_reuse():
    rocket = Rocket(name="Falcon 9", is_active=False, cost_per_launch=50000000, stages=2)
    assert rocket.can_reuse() is False

@pytest.mark.usefixtures("rocket_falcon9")
def test_fixture_rocket(rocket_falcon9):
    """
    Example test that uses the rocket_falcon9 fixture.
    """
    assert rocket_falcon9.name == "Falcon 9"
    assert rocket_falcon9.can_reuse() is True
