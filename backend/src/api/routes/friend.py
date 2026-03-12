from fastapi import APIRouter, status, HTTPException
from src.api.deps import SessionDep, CurrentUser
from src.models.friend_request import FriendRequest
from src.schemas.friend import Invitation
from src import crud

router = APIRouter(tags=["friend"], prefix="/friend")

@router.post("/requests", status_code=status.HTTP_201_CREATED)
def send_friend_request(session: SessionDep, current_user: CurrentUser, invitation: Invitation) -> FriendRequest:
    from_user = current_user.id 
    to_user = invitation.to
    if from_user == to_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't sent friend request to yourself")
    
    if not crud.get_user_by_id(session, to_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    
    if crud.check_friendship(session, from_user, to_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You're already friends")
    
    if crud.check_friend_request(session, from_user, to_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There is already a friend request")
    
    friend_request = crud.create_friend_request(session, from_user, invitation)
    return friend_request