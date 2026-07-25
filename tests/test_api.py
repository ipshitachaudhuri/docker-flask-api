import requests


BASE_URL = "http://localhost:8000"

# Store created user ID for update/delete tests
user_id = None


def test_health():
    response = requests.get(f"{BASE_URL}/health")

    assert response.status_code == 200
    assert response.json()["status"] in ["ok", "healthy"]


def test_database_connection():
    response = requests.get(f"{BASE_URL}/db")

    assert response.status_code == 200
    assert response.json()["database"] == "connected"


def test_create_user():
    global user_id

    response = requests.post(
        f"{BASE_URL}/users",
        json={
            "name": "Test User"
        }
    )

    assert response.status_code == 201

    data = response.json()

    # Save generated user ID
    user_id = data["id"]

    assert user_id is not None


def test_get_users():
    response = requests.get(
        f"{BASE_URL}/users"
    )

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_update_user():
    global user_id

    response = requests.put(
        f"{BASE_URL}/users/{user_id}",
        json={
            "name": "Updated User"
        }
    )

    assert response.status_code == 200


def test_delete_user():
    global user_id

    response = requests.delete(
        f"{BASE_URL}/users/{user_id}"
    )

    assert response.status_code == 200

