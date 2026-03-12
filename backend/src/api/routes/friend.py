from fastapi import APIRouter, status, HTTPException
from src.api.deps import SessionDep, CurrentUser
from src.models.friend_request import FriendRequest
from src.schemas.user import UserPublic
from src.schemas.friend import Invitation
from src import crud
from uuid import UUID
from typing import Any

router = APIRouter(tags=["friend"], prefix="/friend")

@router.post("/requests", status_code=status.HTTP_201_CREATED)
def send_friend_request(session: SessionDep, current_user: CurrentUser, invitation: Invitation) -> FriendRequest:
    from_user = current_user.id 
    to_user = invitation.to
    if from_user == to_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't sent friend request to yourself")
    
    if not crud.get_user_by_id(session, to_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if crud.check_friendship(session, from_user, to_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You're already friends")
    
    if crud.check_friend_request(session, from_user, to_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Friend request already exists")
    
    friend_request = crud.create_friend_request(session, from_user, invitation)
    return friend_request

@router.post("/requests/{request_id}/accept", status_code=status.HTTP_200_OK, response_model=UserPublic)
def accept_friend_request(session: SessionDep, current_user: CurrentUser, request_id: UUID) -> Any:
    user_id = current_user.id
    friend_request = crud.get_request_by_id(session, request_id)
    if not friend_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    
    if friend_request.to_user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    from_user = crud.get_user_by_id(session, friend_request.from_user_id)
    crud.create_friendship(session, friend_request)

    return from_user

@router.post("/requests/{request_id}/decline", status_code=status.HTTP_204_NO_CONTENT)
def decline_friend_request(session: SessionDep, current_user: CurrentUser, request_id: UUID) -> None:
    user_id = current_user.id
    friend_request = crud.get_request_by_id(session, request_id)
    if not friend_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    
    if friend_request.to_user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    crud.delete_friend_req(session, friend_request)