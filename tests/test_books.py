from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_search_books_returns_transformed_results():
    mock_payload = {
        "docs": [
            {
                "key": "/works/OL45804W",
                "title": "Learning Python",
                "author_name": ["Mark Lutz"],
                "first_publish_year": 1999,
                "cover_i": 12345,
            }
        ]
    }

    with patch(
        "app.routers.books.fetch_search_results",
        new=AsyncMock(return_value=mock_payload),
    ):
        response = client.get("/api/books/search?q=python&limit=5")

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "python"
    assert data["limit"] == 5
    assert data["results"][0]["openlibrary_key"] == "/works/OL45804W"
    assert data["results"][0]["cover_url"].endswith("/12345-L.jpg")


def test_get_book_returns_open_library_detail():
    mock_payload = {
        "key": "/works/OL45804W",
        "title": "Learning Python",
        "description": {"value": "A practical guide to Python."},
        "subjects": ["Python", "Programming", "Software Development"],
        "covers": [98765],
        "first_publish_date": "1999",
    }

    with patch(
        "app.routers.books.fetch_work_details",
        new=AsyncMock(return_value=mock_payload),
    ):
        response = client.get("/api/books/OL45804W")

    assert response.status_code == 200
    data = response.json()
    assert data["openlibrary_key"] == "/works/OL45804W"
    assert data["title"] == "Learning Python"
    assert data["subject"] == "Python, Programming, Software Development"
    assert data["description"] == "A practical guide to Python."
