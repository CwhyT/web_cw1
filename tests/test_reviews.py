from uuid import uuid4

from tests.helpers import add_book_to_list, create_reading_list, login_headers, register_user


def test_review_crud_flow(client):
    user_id, email, password = register_user(client, "reviewer")
    headers = login_headers(client, email, password)
    list_id = create_reading_list(client, headers, user_id, "Review Queue", "Books to review")
    item = add_book_to_list(
        client,
        headers,
        list_id,
        key=f"/works/OL{uuid4().hex[:8]}W",
        title="Test Driven Reading",
        author="Alex Reader",
        subject="Software Testing",
    )
    book_id = item["book_id"]

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


def test_create_review_returns_404_for_missing_book(client):
    user_id, email, password = register_user(client, "reviewer_missing_book")
    headers = login_headers(client, email, password)
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
