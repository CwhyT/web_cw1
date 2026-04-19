from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_create_reading_list_flow():
    token = uuid4().hex[:8]
    register_response = client.post(
        "/api/auth/register",
        json={
            "username": f"reader_{token}",
            "email": f"reader_{token}@example.com",
            "password": "secret123",
        },
    )

    assert register_response.status_code == 201
    user_id = register_response.json()["id"]

    create_list_response = client.post(
        "/api/lists",
        json={
            "user_id": user_id,
            "name": "Spring Reads",
            "description": "Books for the next semester break",
        },
    )

    assert create_list_response.status_code == 201
    assert create_list_response.json()["name"] == "Spring Reads"


def test_create_list_returns_404_for_missing_user():
    response = client.post(
        "/api/lists",
        json={
            "user_id": 999999,
            "name": "Missing User List",
            "description": "Should fail",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
