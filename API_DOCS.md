# ShelfSense API Documentation

## Overview

ShelfSense API is a REST API for book discovery, reading list management,
reviews, analytics, and recommendations.

Base URL when running locally:

```text
http://127.0.0.1:8000
```

API prefix:

```text
/api
```

Response format:

- JSON

Authentication:

- Bearer token required for protected write endpoints

## 1. Authentication

### `POST /api/auth/register`

Create a new user account.

Example request:

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "secret123"
}
```

Example response:

```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "created_at": "2026-04-19T13:00:00"
}
```

### `POST /api/auth/login`

Log in and obtain a bearer token.

Example request:

```json
{
  "email": "alice@example.com",
  "password": "secret123"
}
```

Example response:

```json
{
  "access_token": "token_here",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "created_at": "2026-04-19T13:00:00"
  }
}
```

### `GET /api/auth/me`

Return the currently authenticated user.

Required header:

```text
Authorization: Bearer <token>
```

## 2. Books

### `GET /api/books/search`

Search Open Library books by keyword.

Query parameters:

- `q`: search keyword
- `limit`: maximum number of results, default `10`

Example:

```text
GET /api/books/search?q=python&limit=5
```

Example response:

```json
{
  "query": "python",
  "limit": 5,
  "results": [
    {
      "openlibrary_key": "/works/OL45804W",
      "title": "Learning Python",
      "author_name": "Mark Lutz",
      "first_publish_year": 1999,
      "cover_url": "https://covers.openlibrary.org/b/id/12345-L.jpg"
    }
  ]
}
```

### `GET /api/books/{openlibrary_key}`

Fetch a book detail record from Open Library.

Accepted path values:

- `OL45804W`
- `/works/OL45804W`

Example response:

```json
{
  "openlibrary_key": "/works/OL45804W",
  "title": "Learning Python",
  "author_name": null,
  "first_publish_year": null,
  "subject": "Python, Programming, Software Development",
  "cover_url": "https://covers.openlibrary.org/b/id/98765-L.jpg",
  "description": "A practical guide to Python."
}
```

## 3. Reading Lists

These write endpoints require authentication.

### `POST /api/lists`

Create a reading list for the authenticated user.

Example request:

```json
{
  "user_id": 1,
  "name": "Spring Reads",
  "description": "Books for the next semester break"
}
```

### `GET /api/lists`

List reading lists for the authenticated user.

Optional query parameter:

- `user_id`

### `GET /api/lists/{list_id}`

Return one reading list with its saved items.

### `PUT /api/lists/{list_id}`

Update reading list metadata.

Example request:

```json
{
  "name": "Updated List Name",
  "description": "Updated description"
}
```

### `DELETE /api/lists/{list_id}`

Delete a reading list.

### `POST /api/lists/{list_id}/items`

Add a book to a reading list and cache it locally.

Example request:

```json
{
  "openlibrary_key": "/works/OL45804W",
  "title": "Learning Python",
  "author_name": "Mark Lutz",
  "first_publish_year": 1999,
  "subject": "Python, Programming",
  "cover_url": "https://covers.openlibrary.org/b/id/12345-L.jpg",
  "status": "to_read"
}
```

### `PUT /api/lists/{list_id}/items/{item_id}`

Update a saved item status.

Example request:

```json
{
  "status": "finished"
}
```

### `DELETE /api/lists/{list_id}/items/{item_id}`

Remove a book from a reading list.

## 4. Reviews

Protected write endpoints require authentication.

### `POST /api/reviews`

Create a review.

Example request:

```json
{
  "user_id": 1,
  "book_id": 2,
  "rating": 5,
  "review_text": "Helpful and well structured."
}
```

### `GET /api/reviews/{review_id}`

Get one review by id.

### `GET /api/reviews/book/{book_id}`

List all reviews for a book stored in the local database.

### `PUT /api/reviews/{review_id}`

Update a review.

### `DELETE /api/reviews/{review_id}`

Delete a review.

## 5. Analytics

### `GET /api/analytics/genres`

Return the most common subjects across locally cached books.

Example response:

```json
{
  "genres": [
    {
      "name": "Python",
      "count": 4
    },
    {
      "name": "Programming",
      "count": 3
    }
  ]
}
```

### `GET /api/analytics/user/{user_id}/preferences`

Return the user's preferred subjects, authors, and average rating.

### `GET /api/analytics/recommendations/user/{user_id}`

Return rule-based recommendations using saved books and highly rated reviews.

The current strategy:

- boosts subjects from saved books
- boosts authors and subjects from highly rated books
- excludes books the user already saved or reviewed
- returns a recommendation reason for each result

## Error Handling

Common status codes used by the API:

- `200 OK`: successful read or update
- `201 Created`: resource created successfully
- `204 No Content`: resource deleted successfully
- `400 Bad Request`: invalid update payload
- `401 Unauthorized`: missing or invalid authentication token
- `403 Forbidden`: authenticated user tried to modify another user's data
- `404 Not Found`: requested resource does not exist
- `409 Conflict`: duplicate username, email, or book-list relationship
- `502 Bad Gateway`: external Open Library request failed

## Notes

- Book search and book detail endpoints rely on Open Library.
- Analytics and recommendations operate on locally cached book data.
- Swagger UI is available from FastAPI for interactive exploration.
