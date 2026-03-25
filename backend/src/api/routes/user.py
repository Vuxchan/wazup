from fastapi import APIRouter, status, HTTPException, status
from src.api.deps import CurrentUser, SessionDep
from src.schemas.user import UserPublic, UserSearch
from typing import Any
from src import crud

router = APIRouter(tags=["user"], prefix="/users")

@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user

@router.get("/search", status_code=status.HTTP_200_OK, response_model=UserSearch)
def search_user_by_username(session: SessionDep, curr_user: CurrentUser, username: str) -> Any:
    if not username or not username.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is required")
    
    user = crud.get_user_by_username(session, username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user