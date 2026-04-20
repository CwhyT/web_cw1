# ShelfSense API Presentation Outline

## Slide 1: Title

- ShelfSense API
- XJCO3011 Web Services and Web Data
- Individual Coursework Project

## Slide 2: Project Aim

- Build a RESTful book discovery and reading-management API
- Integrate public book data with local SQL-backed CRUD
- Add analytics and recommendation features

## Slide 3: Technology Stack

- FastAPI
- SQLAlchemy
- SQLite
- Open Library
- Pytest

## Slide 4: System Architecture

- Open Library for public book search and detail lookup
- Local database for users, lists, books, and reviews
- Authentication and protected endpoints

## Slide 5: Data Model

- users
- books
- reading_lists
- reading_list_items
- reviews

## Slide 6: Core API Features

- authentication
- book search and detail endpoints
- reading list CRUD
- review CRUD

## Slide 7: Analytics and Recommendations

- genre analytics
- user preference analysis
- rule-based recommendation logic

## Slide 8: Testing and Error Handling

- automated test suite
- validation messages
- ownership checks and authentication failures

## Slide 9: Version Control and Documentation

- GitHub commit history
- README
- API documentation
- manual testing template

## Slide 10: Reflection and Future Work

- what worked well
- current limitations
- possible deployment and future improvements

## Q&A Preparation

Be ready to explain:

- why FastAPI was chosen
- why SQLite was sufficient
- how Open Library is integrated
- how authentication works
- how recommendations are generated
- what GenAI was used for
