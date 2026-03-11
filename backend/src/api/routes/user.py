from fastapi import APIRouter, status
from src.api.deps import CurrentUser
from src.schemas.user import UserPublic
from typing import Any

router = APIRouter(tags=["user"], prefix="/user")

@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user