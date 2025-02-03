import pytest
from app.core.domain.starlink import Starlink

def test_starlink_initialization():
    sat = Starlink(object_name="STARLINK-1234", country_code="US")
    assert sat.object_name == "STARLINK-1234"
    assert sat.country_code == "US"

@pytest.mark.usefixtures("starlink_sat")
def test_fixture_starlink(starlink_sat):
    assert starlink_sat.object_name == "STARLINK-1500"
    assert starlink_sat.country_code == "US"
