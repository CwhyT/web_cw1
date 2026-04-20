# Technical Report: ShelfSense API

**Module:** XJCO3011 Web Services and Web Data  
**Project:** ShelfSense API  
**Project Type:** Individual Coursework  
**Repository:** https://github.com/CwhyT/web_cw1.git  
**External Data Source:** Open Library  

## Submission Materials

This report supports the final coursework submission package. The following materials should be included together in the final Minerva submission:

- **GitHub repository:** https://github.com/CwhyT/web_cw1.git
- **API documentation:** add the final API documentation PDF or repository link here before submission
- **Presentation slides:** add the final PPTX or exported slide link here before submission
- **Deployment status:** currently designed for local execution; no public hosted deployment link is included at this stage
- **Authentication method:** bearer token authentication through `POST /api/auth/login`
- **Current automated test summary:** `16 passed`

The final exported PDF version of this report should retain these navigation details so that an examiner can quickly access the repository, API documentation, slides, and GenAI appendix materials.

## 1. Introduction

ShelfSense API is a RESTful web API for book discovery, reading list management, review storage, user preference analysis, and recommendation generation. The project was developed to satisfy the coursework requirement for a data-driven web service that uses HTTP endpoints, JSON responses, SQL-backed CRUD operations, documentation, testing, and version-controlled development.

The main idea of the project is to combine public book metadata from Open Library with locally stored user activity. Public data is used for live search and book detail retrieval, while local SQL data is used for user accounts, reading lists, reviews, analytics, and recommendations. This approach allows the system to demonstrate both external API integration and relational data modelling in one coherent application.

## 2. Project Scope and Requirements Coverage

The project was designed around three connected use cases:

1. searching for books and viewing book details from a public external source  
2. allowing users to create and manage personal reading lists and reviews  
3. analysing saved activity to generate preference insights and rule-based recommendations  

This scope aligns well with the coursework brief because it naturally supports:

- a SQL-backed data model
- multiple HTTP endpoints
- JSON request and response bodies
- at least one full CRUD resource
- external data integration
- documentation and testing

The final implementation goes beyond the minimum pass requirement because it includes two full CRUD resources, authentication, ownership checks, analytics, and recommendation functionality.

## 3. Technical Stack and Justification

### 3.1 FastAPI

FastAPI was chosen as the backend framework because it is well suited to building RESTful JSON APIs quickly and clearly. It supports declarative request validation through Pydantic, strong typing, and automatic interactive documentation through Swagger UI and ReDoc. This made it suitable both for implementation and for demonstrating the API during testing and presentation.

### 3.2 SQLAlchemy

SQLAlchemy was selected as the ORM because it provides an explicit and maintainable mapping between Python models and relational database tables. This helped keep the database design clear and supported the coursework requirement for SQL-based CRUD functionality.

### 3.3 SQLite

SQLite was used as the main database during development. It was chosen because it is lightweight, easy to set up locally, and appropriate for a coursework-scale prototype. It allowed rapid iteration without introducing deployment or infrastructure complexity. The application design remains portable enough to move to another SQL database such as PostgreSQL in the future.

### 3.4 Open Library

Open Library was selected as the external data source because it provides public book metadata through a straightforward API. It was suitable for book search and detail lookup without requiring the project to maintain a complete local catalogue of book data.

### 3.5 Supporting Libraries

Additional project libraries include:

- **Pydantic** for validation and serialization
- **httpx** for external HTTP requests to Open Library
- **pytest** for automated testing

## 4. System Design

### 4.1 Architectural Approach

The application follows a layered API structure:

- `routers/` for HTTP endpoint definitions
- `models/` for SQLAlchemy database entities
- `schemas/` for validated request and response models
- `services/` for external API integration and recommendation logic
- `tests/` for automated verification

This separation improves maintainability and makes the system easier to explain in both documentation and presentation.

### 4.2 RESTful API Design

The system is implemented as a RESTful API using resource-oriented endpoints and standard HTTP methods:

- `GET` for retrieval
- `POST` for creation
- `PUT` for update
- `DELETE` for deletion

Responses are returned in JSON and conventional status codes are used throughout the system. For example, `201 Created` is returned for successful resource creation, `204 No Content` for successful deletion, and `404 Not Found` for missing resources.

### 4.3 Data Source Strategy

The project uses two data sources:

- **Open Library** for live search and book detail retrieval
- **local SQLite storage** for users, cached books, reading lists, and reviews

This hybrid approach was a deliberate design choice. It keeps the public book dataset external while storing user-owned activity locally, which makes CRUD, analytics, and recommendation logic easier to implement with SQL queries.

## 5. Database Design

The main database tables are:

- `users`
- `books`
- `reading_lists`
- `reading_list_items`
- `reviews`

### 5.1 Table Roles

- `users` stores account and authentication information
- `books` stores cached book records that have been added to reading lists
- `reading_lists` stores user-owned list containers
- `reading_list_items` stores the relationship between lists and books, including reading status
- `reviews` stores user-written ratings and text reviews for locally cached books

### 5.2 Relationships

The main relationships are:

- one user to many reading lists
- one reading list to many reading list items
- one user to many reviews
- one book to many reviews

This schema supports the two main CRUD resources in the project: reading lists and reviews. It also supports analytics by enabling joins between users, books, lists, and ratings.

## 6. Implemented Functionality

The completed API includes the following functional areas.

### 6.1 Authentication

- user registration
- user login
- current user lookup
- bearer token protection for protected endpoints
- ownership checks for lists and reviews

### 6.2 Book Discovery

- book search via Open Library
- single book detail retrieval via Open Library
- normalization of Open Library work keys

### 6.3 Reading Lists

- create reading list
- list reading lists
- view one reading list
- update reading list
- delete reading list

### 6.4 Reading List Items

- add a book to a reading list
- locally cache the book if it is not already stored
- update reading status
- remove a book from a reading list

### 6.5 Reviews

- create review
- retrieve one review
- retrieve all reviews for a local book
- update review
- delete review

### 6.6 Analytics and Recommendations

- genre frequency analysis
- user preference analysis based on saved books and ratings
- rule-based recommendations based on subjects and authors

These features mean the system exceeds the minimum CRUD requirement and demonstrates additional analytical value.

## 7. Security, Validation, and Error Handling

Protected endpoints require a bearer token obtained from the login endpoint. The project enforces ownership checks so that users cannot create or modify another user’s reading lists or reviews.

Validation is handled through Pydantic schemas. The API also includes simplified validation error messages to improve readability. Examples include:

- `Invalid email format`
- `Missing required field: email`
- `Rating must be between 1 and 5`

The system uses conventional HTTP status codes, including:

- `401 Unauthorized` for missing or invalid authentication
- `403 Forbidden` for ownership violations
- `404 Not Found` for missing resources
- `409 Conflict` for duplicates such as repeated registration details or duplicate list-book combinations
- `422 Unprocessable Entity` for validation problems

## 8. Testing Strategy and Evidence

Automated testing was carried out with `pytest` and FastAPI’s `TestClient`. External Open Library calls were mocked so that tests could run reliably without depending on network availability.

The test suite currently reports:

- **16 passed**

### 8.1 Covered Areas

The automated tests cover:

- successful login
- login failure for invalid password
- authentication requirement for `/api/auth/me`
- book search result transformation
- book detail transformation from Open Library payload
- successful reading list creation
- prevention of list creation for another user account
- prevention of access to another user’s list
- review CRUD flow
- rejection of review creation for a missing book
- prevention of deleting another user’s review
- analytics and recommendation endpoints
- concise validation error behaviour
- health endpoint behaviour

### 8.2 Manual Testing

In addition to automated tests, a plain-text manual testing guide was prepared in `manual_test_template.txt`. This includes copyable PowerShell examples for endpoint testing and was useful for manual verification during development.

## 9. Challenges and Solutions

### 9.1 Combining External and Local Data

One challenge was balancing a public external dataset with a local SQL data model. This was addressed by using Open Library only for live search and detail lookup, while caching selected books locally once they were added to reading lists. This allowed analytics and reviews to operate on stable local data.

### 9.2 Authentication and Ownership

Another challenge was ensuring the project was not just an open CRUD prototype. The solution was to introduce bearer-token authentication and ownership checks so that users can only access or modify their own lists and reviews.

### 9.3 Recommendation Logic

A further challenge was implementing recommendations in a way that was useful but still appropriate for a coursework timescale. Instead of using machine learning, the project uses a rule-based strategy that increases weights for preferred subjects and authors derived from saved books and highly rated reviews.

## 10. Lessons Learned

The project highlighted several practical lessons about API development.

First, combining an external API with a local SQL database is often more effective than trying to store everything in one place. Open Library worked well for live discovery, while the local relational database was much better suited to user-owned state such as reading lists, cached books, and reviews.

Second, authentication and ownership checks are essential if an API is intended to represent real user data rather than a simple demonstration prototype. Adding bearer-token authentication and user-level permission checks made the API more realistic and improved the quality of the design beyond minimum CRUD functionality.

Third, testing and documentation are not just supporting tasks but part of the core engineering work. Automated tests helped verify authentication, permissions, and analytics behaviour, while written API documentation and report drafting exposed inconsistencies that would have been harder to notice through coding alone.

## 11. Limitations

The project has several current limitations:

- it is designed primarily for local execution with SQLite
- no hosted deployment is currently included
- the recommendation system is rule-based rather than machine-learning-based
- there is no frontend client
- live book search and detail retrieval depend on Open Library availability

These limitations do not prevent the system from meeting the core coursework requirements, but they do define the current scope of the implementation.

## 12. Future Improvements

If the project were extended further, the following improvements would be most valuable:

- deploy the API to a public hosting platform
- migrate from SQLite to PostgreSQL for production use
- replace the lightweight token mechanism with a stronger JWT implementation
- improve recommendation ranking and diversity
- extend analytics with richer summaries or dashboards
- produce a more polished exported API documentation PDF

## 13. Coursework Deliverables Status

At code level, the project already satisfies the major technical requirements:

- SQL-backed CRUD resources are implemented
- more than four HTTP endpoints are available
- JSON responses are used throughout
- external API integration is implemented
- error handling and status codes are present
- automated testing evidence exists
- GitHub version history exists

Supporting coursework documents have also been prepared in draft or near-final form, including:

- API documentation
- README
- presentation outline
- submission report draft

However, before final submission, the report PDF should explicitly include:

- the GitHub repository link
- the API documentation link or attached PDF reference
- the presentation slides link or attached slide reference
- the GenAI declaration
- the GenAI analysis/reflection
- a conversation-log appendix or clearly attached supplementary examples

## 14. GenAI Declaration and Reflection

Generative AI tools were used in a declared and supportive capacity during this coursework. Their role included planning assistance, translation and interpretation of the coursework brief, documentation drafting, debugging support, code review assistance, and identification of missing requirements or testing gaps.

AI was not used as an unreviewed substitute for project ownership. Suggestions were manually reviewed, adapted where necessary, and verified through local testing and repository inspection before being retained.

The most useful role of GenAI in this project was accelerating planning and documentation refinement, while also helping identify missing requirements such as authentication hardening, test coverage gaps, and incomplete submission materials. However, all implementation decisions still required manual validation to ensure correctness and alignment with the brief.

### 14.1 Declared Tools and Purposes

| Tool | Purpose | Example Use in This Project | Human Verification |
|---|---|---|---|
| ChatGPT | coursework interpretation, planning, writing support | translating and analysing the brief, structuring the report, identifying missing deliverables | outputs were checked against the brief and rewritten where needed |
| Codex | repository assistance, implementation support, debugging, test improvement | building routes, refining validation messages, improving tests, cleaning the repository, drafting documentation | all code and document changes were inspected locally and tested before retention |
| Microsoft Word or equivalent editor | report editing and export | formatting report text, preparing final PDF-ready submission document | final wording and layout remain the student’s responsibility |

### 14.2 GenAI Use Analysis

GenAI was most effective in three areas. First, it accelerated early-stage planning by helping convert the brief into a concrete sequence of implementation steps. Second, it improved the quality and coverage of documentation by highlighting missing sections such as API completeness, submission materials, and declaration content. Third, it supported debugging and review by identifying inconsistent endpoint documentation, missing tests, and permission edge cases.

At the same time, GenAI output could not be accepted blindly. API behaviour, file paths, course compliance, and repository state all required manual checking. This project therefore used GenAI as a drafting and review assistant rather than as a replacement for implementation ownership.

### 14.3 Conversation Log Appendix

The final submission should include representative conversation-log evidence as supplementary material. This appendix should show examples of:

- coursework brief interpretation
- topic and data-source selection
- API design planning
- debugging or validation-error refinement
- documentation and submission-material review

In the final PDF or supplementary appendix, this should be attached as either:

- exported conversation text snippets
- screenshots of selected exchanges
- or a separate appendix PDF referenced clearly from this report

This appendix is a required declared part of the final GenAI submission evidence and should not be left implicit.

## 15. Conclusion

ShelfSense API demonstrates a complete API development workflow from project scoping and database design to CRUD implementation, authentication, testing, analytics, and supporting documentation. It satisfies the core coursework expectations for a RESTful, SQL-backed web service and goes beyond the minimum requirement through recommendation features, access control, and structured testing. The current implementation is functional, documented, and ready to be packaged into the final coursework submission.

## References

1. Open Library, n.d. *Open Library Developers*. Available at: https://openlibrary.org/developers (Accessed: 20 April 2026).  
2. FastAPI, n.d. *FastAPI Documentation*. Available at: https://fastapi.tiangolo.com/ (Accessed: 20 April 2026).  
3. SQLAlchemy, n.d. *SQLAlchemy Documentation*. Available at: https://docs.sqlalchemy.org/ (Accessed: 20 April 2026).  
