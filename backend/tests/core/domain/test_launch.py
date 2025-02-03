import pytest
from app.core.domain.launch import Launch

def test_launch_initialization():
    launch = Launch(details="Test Launch", success=True, rocket_id=1)
    assert launch.details == "Test Launch"
    assert launch.success is True
    assert launch.rocket_id == 1

def test_is_successful():
    launch = Launch(details="Another Launch", success=True, rocket_id=2)
    assert launch.is_successful() is True

@pytest.mark.usefixtures("launch_demo")
def test_fixture_launch(launch_demo):
    assert launch_demo.details == "Demo Launch"
    assert launch_demo.is_successful() is True
