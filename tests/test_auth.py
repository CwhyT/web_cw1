from uuid import uuid4

def test_login_returns_token_and_current_user(client):
    token = uuid4().hex[:8]
    email = f"auth_{token}@example.com"
    password = "secret123"

    register_response = client.post(
        "/api/auth/register",
        json={
            "username": f"auth_{token}",
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
    token_value = login_response.json()["access_token"]

    me_response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token_value}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == email


def test_login_rejects_invalid_password(client):
    token = uuid4().hex[:8]
    email = f"auth_fail_{token}@example.com"

    register_response = client.post(
        "/api/auth/register",
        json={
            "username": f"auth_fail_{token}",
            "email": email,
            "password": "correct-password",
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={"email": email, "password": "wrong-password"},
    )
    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Invalid email or password"


def test_me_requires_authentication(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"
