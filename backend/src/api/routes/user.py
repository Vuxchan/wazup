from fastapi import APIRouter, status, HTTPException, status, UploadFile
from src.api.deps import CurrentUser, SessionDep, ValidateDep
from src.schemas.user import UserPublic, UserDisplay
from typing import Any
from src import crud
from src.core.cloudinary import upload_img

router = APIRouter(tags=["user"], prefix="/users")

@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user

@router.get("/search", status_code=status.HTTP_200_OK, response_model=UserDisplay)
def search_user_by_username(session: SessionDep, current_user: CurrentUser, username: str) -> Any:
    if not username or not username.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is required")
    
    user = crud.get_user_by_username(session, username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user

@router.post("/avatar", status_code=status.HTTP_200_OK)
async def upload_avatar(session: SessionDep, current_user: CurrentUser, validated_img: ValidateDep) -> str:
    if not validated_img:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded")
    
    result = await upload_img(validated_img, current_user.id)

    crud.update_avatar(session, result["secure_url"], result["public_id"], current_user)

    avatar_url = current_user.avatar_url
    if not avatar_url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Null avatar")
    
    return avatar_url