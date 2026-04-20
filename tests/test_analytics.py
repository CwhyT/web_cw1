from uuid import uuid4

from tests.helpers import add_book_to_list, create_reading_list, login_headers, register_user


def test_user_preferences_and_recommendations(client):
    favorite_title = f"Python Patterns {uuid4().hex[:6]}"
    user_id, email, password = register_user(client, "analytics_user")
    headers = login_headers(client, email, password)
    own_list_id = create_reading_list(client, headers, user_id, "Favorites")

    favorite_book = add_book_to_list(
        client,
        headers,
        own_list_id,
        key=f"/works/OL{uuid4().hex[:8]}W",
        title=favorite_title,
        author="Alex Reader",
        subject="Python, Programming",
    )
    favorite_book_id = favorite_book["book_id"]
    client.post(
        "/api/reviews",
        json={
            "user_id": user_id,
            "book_id": favorite_book_id,
            "rating": 5,
            "review_text": "Exactly my kind of technical book.",
        },
        headers=headers,
    )

    other_user_id, other_email, other_password = register_user(client, "analytics_other")
    other_headers = login_headers(client, other_email, other_password)
    other_list_id = create_reading_list(client, other_headers, other_user_id, "Shared Shelf")
    add_book_to_list(
        client,
        other_headers,
        other_list_id,
        key=f"/works/OL{uuid4().hex[:8]}W",
        title=f"Advanced Python Systems {uuid4().hex[:6]}",
        author="Chris Builder",
        subject="Python, Software Engineering",
    )
    add_book_to_list(
        client,
        other_headers,
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
    assert all(item["reason"] for item in recommendations_data)
    assert any("preferred" in item["reason"] or "author" in item["reason"] for item in recommendations_data)


def test_genre_analytics_returns_subject_counts(client):
    response = client.get("/api/analytics/genres")
    assert response.status_code == 200
    assert isinstance(response.json()["genres"], list)
