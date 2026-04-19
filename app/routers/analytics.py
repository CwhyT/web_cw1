from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/genres")
def genre_analytics_placeholder() -> dict[str, list]:
    return {"genres": []}


@router.get("/user/{user_id}/preferences")
def user_preferences_placeholder(user_id: int):
    return {
        "user_id": user_id,
        "favorite_subjects": [],
        "favorite_authors": [],
        "average_rating": None,
    }


@router.get("/recommendations/user/{user_id}")
def recommendations_placeholder(user_id: int):
    return {"user_id": user_id, "recommendations": []}

