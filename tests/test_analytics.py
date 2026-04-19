from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _register_user(prefix: str) -> int:
    token = uuid4().hex[:8]
    response = client.post(
        "/api/auth/register",
        json={
            "username": f"{prefix}_{token}",
            "email": f"{prefix}_{token}@example.com",
            "password": "secret123",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def _create_list(user_id: int, name: str) -> int:
    response = client.post(
        "/api/lists",
        json={"user_id": user_id, "name": name, "description": f"{name} description"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def _add_book(list_id: int, *, key: str, title: str, author: str, subject: str) -> int:
    response = client.post(
        f"/api/lists/{list_id}/items",
        json={
            "openlibrary_key": key,
            "title": title,
            "author_name": author,
            "first_publish_year": 2024,
            "subject": subject,
            "cover_url": "https://example.com/cover.jpg",
            "status": "finished",
        },
    )
    assert response.status_code == 201
    return response.json()["book_id"]


def test_user_preferences_and_recommendations():
    user_id = _register_user("analytics_user")
    own_list_id = _create_list(user_id, "Favorites")

    favorite_book_id = _add_book(
        own_list_id,
        key=f"/works/OL{uuid4().hex[:8]}W",
        title="Python Patterns",
        author="Alex Reader",
        subject="Python, Programming",
    )
    client.post(
        "/api/reviews",
        json={
            "user_id": user_id,
            "book_id": favorite_book_id,
            "rating": 5,
            "review_text": "Exactly my kind of technical book.",
        },
    )

    other_user_id = _register_user("analytics_other")
    other_list_id = _create_list(other_user_id, "Shared Shelf")
    _add_book(
        other_list_id,
        key=f"/works/OL{uuid4().hex[:8]}W",
        title="Advanced Python Systems",
        author="Chris Builder",
        subject="Python, Software Engineering",
    )
    _add_book(
        other_list_id,
        key=f"/works/OL{uuid4().hex[:8]}W",
        title="History of Architecture",
        author="Dana Stone",
        subject="History, Architecture",
    )

    preferences_response = client.get(f"/api/analytics/user/{user_id}/preferences")
    assert preferences_response.status_code == 200
    preferences_data = preferences_response.json()
    assert "Python" in preferences_data["favorite_subjects"]
    assert "Alex Reader" in preferences_data["favorite_authors"]
    assert preferences_data["average_rating"] == 5.0

    recommendations_response = client.get(f"/api/analytics/recommendations/user/{user_id}")
    assert recommendations_response.status_code == 200
    recommendations_data = recommendations_response.json()["recommendations"]
    assert len(recommendations_data) >= 1
    assert recommendations_data[0]["title"] == "Advanced Python Systems"


def test_genre_analytics_returns_subject_counts():
    response = client.get("/api/analytics/genres")
    assert response.status_code == 200
    assert isinstance(response.json()["genres"], list)
