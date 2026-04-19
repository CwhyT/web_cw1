from fastapi import FastAPI

from app.database import Base, engine
from app import models  # noqa: F401
from app.routers import analytics, auth, books, lists, reviews


def create_application() -> FastAPI:
    app = FastAPI(
        title="ShelfSense API",
        description="Book search, reading list, review, and analytics API.",
        version="0.1.0",
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(auth.router, prefix="/api")
    app.include_router(books.router, prefix="/api")
    app.include_router(lists.router, prefix="/api")
    app.include_router(reviews.router, prefix="/api")
    app.include_router(analytics.router, prefix="/api")

    @app.get("/", tags=["root"])
    def read_root() -> dict[str, str]:
        return {"message": "Welcome to ShelfSense API"}

    @app.get("/health", tags=["health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_application()
