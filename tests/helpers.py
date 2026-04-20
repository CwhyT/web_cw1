from uuid import uuid4

from fastapi.testclient import TestClient


def register_user(
    client: TestClient,
    prefix: str,
    password: str = "secret123",
) -> tuple[int, str, str]:
    token = uuid4().hex[:8]
    email = f"{prefix}_{token}@example.com"
    response = client.post(
        "/api/auth/register",
        json={
            "username": f"{prefix}_{token}",
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == 201
    return response.json()["id"], email, password


def login_headers(client: TestClient, email: str, password: str) -> dict[str, str]:
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_reading_list(
    client: TestClient,
    headers: dict[str, str],
    user_id: int,
    name: str,
    description: str | None = None,
) -> int:
    response = client.post(
        "/api/lists",
        json={
            "user_id": user_id,
            "name": name,
            "description": description or f"{name} description",
        },
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()["id"]


def add_book_to_list(
    client: TestClient,
    headers: dict[str, str],
    list_id: int,
    *,
    key: str,
    title: str,
    author: str,
    subject: str,
    status: str = "finished",
    first_publish_year: int = 2024,
    cover_url: str = "https://example.com/cover.jpg",
) -> dict:
    response = client.post(
        f"/api/lists/{list_id}/items",
        json={
            "openlibrary_key": key,
            "title": title,
            "author_name": author,
            "first_publish_year": first_publish_year,
            "subject": subject,
            "cover_url": cover_url,
            "status": status,
        },
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()
