import pytest
from app.core.domain.rocket import Rocket
from app.core.domain.launch import Launch
from app.core.domain.starlink import Starlink

@pytest.fixture
def rocket_falcon9():
    """Returns a Rocket domain object with placeholder values."""
    return Rocket(
        name="Falcon 9",
        is_active=True,
        cost_per_launch=50000000,  # 50M
        stages=2
    )

@pytest.fixture
def launch_demo():
    """Returns a Launch domain object with placeholder values."""
    return Launch(
        details="Demo Launch",
        success=True,
        rocket_id=1
    )

@pytest.fixture
def starlink_sat():
    """Returns a Starlink domain object with placeholder values."""
    return Starlink(
        object_name="STARLINK-1500",
        country_code="US"
    )
