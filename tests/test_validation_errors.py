from uuid import uuid4

def test_register_returns_short_email_error(client):
    response = client.post(
        "/api/auth/register",
        json={"username": "cyt", "email": "123", "password": "123"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid email format"


def test_review_returns_short_rating_error(client):
    token = uuid4().hex[:8]
    email = f"validation_{token}@example.com"
    password = "secret123"
    register_response = client.post(
        "/api/auth/register",
        json={
            "username": f"validation_{token}",
            "email": email,
            "password": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}

    response = client.put(
        "/api/reviews/1",
        json={"rating": 8},
        headers=headers,
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Rating must be between 1 and 5"
