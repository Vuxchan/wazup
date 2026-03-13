from sqlmodel import SQLModel
from uuid import UUID
from typing import Optional, TYPE_CHECKING, List
from src.models.friend_request import FriendRequest
from .user import UserPublic

class Invitation(SQLModel):
    to: UUID
    request_message: Optional[str]

class FriendRequests(SQLModel):
    received: List[FriendRequest]
    sent: List[FriendRequest] 

class FriendRequestsResponse(SQLModel):
    received: List[UserPublic]
    sent: List[UserPublic] 