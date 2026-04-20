from tests.helpers import login_headers, register_user


def test_register_and_create_reading_list_flow(client):
    user_id, email, password = register_user(client, "reader")
    headers = login_headers(client, email, password)

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


def test_create_list_rejects_other_user_id(client):
    _, email, password = register_user(client, "reader_missing")
    headers = login_headers(client, email, password)

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
