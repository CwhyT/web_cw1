from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _create_user() -> int:
    token = uuid4().hex[:8]
    response = client.post(
        "/api/auth/register",
        json={
            "username": f"reviewer_{token}",
            "email": f"reviewer_{token}@example.com",
            "password": "secret123",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def _create_list_with_book(user_id: int) -> tuple[int, int]:
    list_response = client.post(
        "/api/lists",
        json={
            "user_id": user_id,
            "name": "Review Queue",
            "description": "Books to review",
        },
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
    )
    assert item_response.status_code == 201
    return list_id, item_response.json()["book_id"]


def test_review_crud_flow():
    user_id = _create_user()
    _, book_id = _create_list_with_book(user_id)

    create_response = client.post(
        "/api/reviews",
        json={
            "user_id": user_id,
            "book_id": book_id,
            "rating": 5,
            "review_text": "Helpful and well structured.",
        },
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
    )
    assert update_response.status_code == 200
    assert update_response.json()["rating"] == 4

    list_response = client.get(f"/api/reviews/book/{book_id}")
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 1

    delete_response = client.delete(f"/api/reviews/{review_id}")
    assert delete_response.status_code == 204


def test_create_review_returns_404_for_missing_book():
    user_id = _create_user()
    response = client.post(
        "/api/reviews",
        json={
            "user_id": user_id,
            "book_id": 999999,
            "rating": 4,
            "review_text": "Should fail",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
