import os
import requests
import psycopg2


BASE_URL = "http://localhost:8000"


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )


def test_health():
    response = requests.get(f"{BASE_URL}/health")

    assert response.status_code == 200
    assert response.json()["status"] in ["ok", "healthy"]


def test_database_connection():
    response = requests.get(f"{BASE_URL}/db")

    assert response.status_code == 200
    assert response.json()["database"] == "connected"


def test_create_user():

    response = requests.post(
        f"{BASE_URL}/users",
        json={
            "name": "Test User"
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
        f"{BASE_URL}/users/1",
        json={
            "name": "Updated User"
        }
    )

    assert response.status_code == 200


def test_delete_user():

    response = requests.delete(
        f"{BASE_URL}/users/1"
    )

    assert response.status_code == 200

