import json
import pytest
from app import app  # Import the app from app.py

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_valid_jwt(client):
    response = client.post('/auth', json={'username': 'helloworld', 'password': 'hellohello'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data

def test_missing_credentials(client):
    response = client.post('/auth', json={})
    assert response.status_code == 400  # Adjust based on your API's response
