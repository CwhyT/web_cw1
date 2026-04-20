# ShelfSense API

ShelfSense API is a coursework project for `XJCO3011 Web Services and Web Data`.
It provides book search, reading list management, reviews, analytics, and
recommendation endpoints backed by a SQL database and Open Library data.

## Overview

ShelfSense API is a data-driven REST API for book discovery and personal reading
management. The project combines:

- public book metadata from Open Library
- local SQL storage for user accounts, reading lists, cached books, and reviews
- analytics endpoints for user preferences and genre trends
- recommendation endpoints based on saved books and ratings

The API was designed to satisfy the coursework requirements for:

- CRUD operations backed by a SQL database
- HTTP endpoints with JSON responses
- correct error handling and status codes
- external data integration
- clear documentation and version-controlled development

## Coursework Context

This repository contains the implementation for an individual API development
project. The system was designed to demonstrate:

- resource-oriented RESTful API design
- SQL-backed CRUD operations
- external API integration
- authentication and protected endpoints
- analytics and recommendation functionality
- automated testing and reproducible local setup

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- httpx
- pytest

## Project Structure

```text
app/
  main.py
  database.py
  models/
  routers/
  schemas/
  services/
  utils/
tests/
requirements.txt
```

## Features

- User registration, login, and bearer-token authentication
- Open Library book search and book detail lookup
- Reading list CRUD operations
- Reading list item management
- Review CRUD operations
- Genre analytics across cached books
- User preference analysis based on saved books and reviews
- Basic rule-based recommendations

## Data Model

The main database tables are:

- `users`
- `books`
- `reading_lists`
- `reading_list_items`
- `reviews`

The local `books` table acts as a cache for books that users save into reading
lists, allowing analytics and recommendation features to work on local data.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

After startup:

- API root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Manual Testing

For manual terminal-based testing, see `manual_test_template.txt`.

That file contains:

- copyable PowerShell request examples
- example values for `user_id`, `book_id`, and route parameters
- notes on which fields should be changed during testing

## Running Tests

```bash
python -m pytest
```

## Authentication

Protected endpoints use Bearer token authentication.

Typical flow:

1. Register a user with `POST /api/auth/register`
2. Log in with `POST /api/auth/login`
3. Copy the returned `access_token`
4. Send the header:

```text
Authorization: Bearer <your_token>
```

## Key Endpoints

Authentication:

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

Books:

- `GET /api/books/search`
- `GET /api/books/{openlibrary_key}`

Reading lists:

- `POST /api/lists`
- `GET /api/lists`
- `GET /api/lists/{list_id}`
- `PUT /api/lists/{list_id}`
- `DELETE /api/lists/{list_id}`
- `POST /api/lists/{list_id}/items`
- `PUT /api/lists/{list_id}/items/{item_id}`
- `DELETE /api/lists/{list_id}/items/{item_id}`

Reviews:

- `POST /api/reviews`
- `GET /api/reviews/{review_id}`
- `GET /api/reviews/book/{book_id}`
- `PUT /api/reviews/{review_id}`
- `DELETE /api/reviews/{review_id}`

Analytics:

- `GET /api/analytics/genres`
- `GET /api/analytics/user/{user_id}/preferences`
- `GET /api/analytics/recommendations/user/{user_id}`

## Documentation

- `API_DOCS.md`: written endpoint summary with example requests and responses
- Swagger UI: interactive documentation at `/docs`
- ReDoc: alternative generated documentation at `/redoc`

## Data Source

This project uses Open Library as the external public book data source:

- Open Library search endpoint
- Open Library work detail endpoint

Locally cached book data is then used for:

- reading list storage
- review storage
- genre analytics
- user preference analysis
- rule-based recommendations

## Current Status

Implemented:

- project skeleton and database integration
- authentication and access control
- book search and detail lookup
- reading list CRUD
- review CRUD
- analytics and recommendation endpoints
- automated API tests
- written API documentation draft

Current automated test status:

- `16 passed`

## Known Limitations

- The project is currently designed for local execution with SQLite.
- Recommendation logic is rule-based rather than machine-learning-based.
- Open Library availability affects live search and book detail responses.
- Pytest cache warnings may still appear in this environment because of local filesystem permissions.

## Repository Notes

- `app/`: application source code
- `tests/`: automated test suite
- `API_DOCS.md`: endpoint documentation draft
- `manual_test_template.txt`: plain-text manual testing guide
- `brief_translation_zh.md`: translated coursework brief used during planning

## Next Submission Tasks

The core API implementation is complete, but the following coursework materials
still need to be finalized outside this README:

- technical report PDF
- API documentation PDF export
- presentation slides
- GenAI declaration and conversation-log appendix
- final submission packaging for Minerva
