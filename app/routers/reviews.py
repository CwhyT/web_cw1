from fastapi import APIRouter

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("")
def create_review_placeholder() -> dict[str, str]:
    return {"message": "Create review placeholder"}


@router.get("/{review_id}")
def get_review_placeholder(review_id: int):
    return {"review_id": review_id, "message": "Get review placeholder"}


@router.put("/{review_id}")
def update_review_placeholder(review_id: int):
    return {"review_id": review_id, "message": "Update review placeholder"}


@router.delete("/{review_id}")
def delete_review_placeholder(review_id: int):
    return {"review_id": review_id, "message": "Delete review placeholder"}

