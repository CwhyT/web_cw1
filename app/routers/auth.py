from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register_placeholder() -> dict[str, str]:
    return {"message": "Register endpoint placeholder"}


@router.post("/login")
def login_placeholder() -> dict[str, str]:
    return {"message": "Login endpoint placeholder"}

