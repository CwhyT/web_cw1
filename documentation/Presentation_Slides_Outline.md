# ShelfSense API Presentation Slides Outline

This file is the presentation-material companion to the API documentation and technical report.
It is stored in the `documentation/` folder so that all main coursework documents are grouped together.

## Slide 1: Title

- ShelfSense API
- XJCO3011 Web Services and Web Data
- Individual Coursework Project

## Slide 2: Project Aim

- Build a RESTful book discovery and reading-management API
- Combine public Open Library data with local SQL-backed CRUD
- Add analytics and rule-based recommendation features

## Slide 3: Technology Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- httpx
- pytest

## Slide 4: System Architecture

- Open Library for public search and detail lookup
- Local database for users, books, reading lists, list items, and reviews
- Bearer-token authentication for protected write endpoints

## Slide 5: Data Model

- `users`
- `books`
- `reading_lists`
- `reading_list_items`
- `reviews`

## Slide 6: Core API Features

- registration and login
- book search and detail endpoints
- reading list CRUD
- review CRUD

## Slide 7: Analytics and Recommendations

- genre analytics
- user preference analysis
- rule-based recommendations based on subjects and authors

## Slide 8: Testing and Validation

- automated testing with `pytest`
- current result: `16 passed`
- concise validation messages
- ownership and authentication checks

## Slide 9: Documentation and Version Control

- GitHub repository with commit history
- API documentation PDF
- technical report PDF
- manual testing template

## Slide 10: Limitations and Future Work

- local execution only
- SQLite for coursework-scale development
- rule-based recommendations
- potential future deployment and stronger authentication

## Presenter Notes

Be prepared to explain:

- why FastAPI was chosen
- why SQLite was suitable for this coursework
- how Open Library is integrated
- how bearer-token authentication works
- how recommendations are generated
- how GenAI was used and reviewed

## Submission Note

If the final coursework submission requires a `.pptx` or exported slide PDF, this outline should be converted into that final format before submission.
