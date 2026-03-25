from sqlmodel import SQLModel
from uuid import UUID
from typing import Optional, List
from src.models.friend_request import FriendRequest
from .user import UserPublic
from src.utils import config

class FriendRequestCreate(SQLModel):
    model_config = config

    to: UUID
    request_message: Optional[str]

class FriendRequestFilter(SQLModel):
    received: List[FriendRequest]
    sent: List[FriendRequest] 

class FriendRequestUsersPublic(SQLModel):
    received: List[UserPublic]
    sent: List[UserPublic] 