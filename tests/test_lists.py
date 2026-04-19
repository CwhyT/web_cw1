from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _login(email: str, password: str) -> dict[str, str]:
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_and_create_reading_list_flow():
    token = uuid4().hex[:8]
    email = f"reader_{token}@example.com"
    password = "secret123"
    register_response = client.post(
        "/api/auth/register",
        json={
            "username": f"reader_{token}",
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 201
    user_id = register_response.json()["id"]
    headers = _login(email, password)

    create_list_response = client.post(
        "/api/lists",
        json={
            "user_id": user_id,
            "name": "Spring Reads",
            "description": "Books for the next semester break",
        },
        headers=headers,
    )

    assert create_list_response.status_code == 201
    assert create_list_response.json()["name"] == "Spring Reads"


def test_create_list_returns_404_for_missing_user():
    token = uuid4().hex[:8]
    email = f"reader_missing_{token}@example.com"
    password = "secret123"
    register_response = client.post(
        "/api/auth/register",
        json={
            "username": f"reader_missing_{token}",
            "email": email,
            "password": password,
        },
    )
    assert register_response.status_code == 201
    headers = _login(email, password)

    response = client.post(
        "/api/lists",
        json={
            "user_id": 999999,
            "name": "Missing User List",
            "description": "Should fail",
        },
        headers=headers,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You can only create lists for your own account"
