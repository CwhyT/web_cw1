from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _create_user() -> tuple[int, str, str]:
    token = uuid4().hex[:8]
    email = f"reviewer_{token}@example.com"
    password = "secret123"
    response = client.post(
        "/api/auth/register",
        json={
            "username": f"reviewer_{token}",
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == 201
    return response.json()["id"], email, password


def _auth_headers(email: str, password: str) -> dict[str, str]:
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def _create_list_with_book(user_id: int, headers: dict[str, str]) -> tuple[int, int]:
    list_response = client.post(
        "/api/lists",
        json={
            "user_id": user_id,
            "name": "Review Queue",
            "description": "Books to review",
        },
        headers=headers,
    )
    assert list_response.status_code == 201
    list_id = list_response.json()["id"]

    item_response = client.post(
        f"/api/lists/{list_id}/items",
        json={
            "openlibrary_key": f"/works/OL{uuid4().hex[:8]}W",
            "title": "Test Driven Reading",
            "author_name": "Alex Reader",
            "first_publish_year": 2024,
            "subject": "Software Testing",
            "cover_url": "https://example.com/cover.jpg",
            "status": "finished",
        },
        headers=headers,
    )
    assert item_response.status_code == 201
    return list_id, item_response.json()["book_id"]


def test_review_crud_flow():
    user_id, email, password = _create_user()
    headers = _auth_headers(email, password)
    _, book_id = _create_list_with_book(user_id, headers)

    create_response = client.post(
        "/api/reviews",
        json={
            "user_id": user_id,
            "book_id": book_id,
            "rating": 5,
            "review_text": "Helpful and well structured.",
        },
        headers=headers,
    )

    assert create_response.status_code == 201
    review_id = create_response.json()["id"]
    assert create_response.json()["rating"] == 5

    get_response = client.get(f"/api/reviews/{review_id}")
    assert get_response.status_code == 200
    assert get_response.json()["book_id"] == book_id

    update_response = client.put(
        f"/api/reviews/{review_id}",
        json={"rating": 4, "review_text": "Still good, but slightly repetitive."},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["rating"] == 4

    list_response = client.get(f"/api/reviews/book/{book_id}")
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 1

    delete_response = client.delete(f"/api/reviews/{review_id}", headers=headers)
    assert delete_response.status_code == 204


def test_create_review_returns_404_for_missing_book():
    user_id, email, password = _create_user()
    headers = _auth_headers(email, password)
    response = client.post(
        "/api/reviews",
        json={
            "user_id": user_id,
            "book_id": 999999,
            "rating": 4,
            "review_text": "Should fail",
        },
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
