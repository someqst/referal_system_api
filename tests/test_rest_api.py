import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def test_user():
    return {
        "email": "some@mail.ru",
        "password": 1234456543
    }


def register(test_user):
    with TestClient(app=app) as client:
        response = client.post('/api/v1/register', json=test_user)
        assert response.status_code == 200
        data = response.json()
        assert data['message'] == "You have successfully registered!"


def login(test_user):
    with TestClient(app=app) as client:
        response = client.post('/api/v1/login', json=test_user)
        assert response.status_code == 200
        data = response.json()
        assert data['message'] == "You have successfully logged in!"


def create_code():
    with TestClient(app=app) as client:
        response = client.post('/api/v1/create_code', code='ahhaha123')
        assert response.status_code == 200
        data = response.json()
        assert data['message'] == 'Code successfully created!'


def logout():
    with TestClient(app=app) as client:
        response = client.post('/api/v1/logout')
        assert response.status_code == 200
        data = response.json()
        assert data['message'] == "You are successfully logged out!"
