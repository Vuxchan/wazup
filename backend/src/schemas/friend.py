from sqlmodel import SQLModel
from uuid import UUID
from typing import Optional, List
from src.models.friend_request import FriendRequest
from .user import UserPublic

class FriendRequestCreate(SQLModel):
    to: UUID
    request_message: Optional[str]

class FriendRequestFilter(SQLModel):
    received: List[FriendRequest]
    sent: List[FriendRequest] 

class FriendRequestPublic(SQLModel):
    received: List[UserPublic]
    sent: List[UserPublic] 