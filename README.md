# ShelfSense API

ShelfSense API is a coursework project for `XJCO3011 Web Services and Web Data`.
It provides book search, reading list management, reviews, analytics, and
recommendation endpoints backed by a SQL database and Open Library data.

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

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Development Status

Current stage:

- Project skeleton created
- Database configuration added
- Router placeholders added
- Ready for model and CRUD implementation
