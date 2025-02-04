import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_list_rockets():
    """Test listing rockets returns a valid response."""
    response = client.get("/api/rockets/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
