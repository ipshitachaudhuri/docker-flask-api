import requests

BASE_URL = "http://localhost:8000"


def test_health():
    response = requests.get(f"{BASE_URL}/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_database_connection():
    response = requests.get(f"{BASE_URL}/db")

    assert response.status_code == 200
    assert response.json()["database"] == "connected"


def test_create_user():

    response = requests.post(
        f"{BASE_URL}/users",
        json={
            "name": "Test User",
            "email": "test@example.com"
        }
    )

    assert response.status_code == 201


def test_get_users():

    response = requests.get(
        f"{BASE_URL}/users"
    )

    assert response.status_code == 200


def test_update_user():

    response = requests.put(
        f"{BASE_URL}/users/5",
        json={
            "name": "Updated User",
            "email": "updated@example.com"
        }
    )

    assert response.status_code == 200


def test_delete_user():

    response = requests.delete(
        f"{BASE_URL}/users/5"
    )

    assert response.status_code == 200
