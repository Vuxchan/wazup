from sqlmodel import SQLModel
from uuid import UUID
from typing import Optional, List
from src.models.friend_request import FriendRequest
from .user import UserDisplay
from src.utils import config
from datetime import datetime

class FriendRequestCreate(SQLModel):
    model_config = config

    to: UUID
    request_message: Optional[str]

class FriendRequestFilter(SQLModel):
    received: List[FriendRequest]
    sent: List[FriendRequest] 

class FriendRequestBase(SQLModel):
    model_config = config

    id: UUID
    request_message: str
    created_at: datetime

class ReceivedRequestPublic(FriendRequestBase):
    @classmethod
    def from_received_request(cls, request: FriendRequest) -> "ReceivedRequestPublic":
        return cls(
            id=request.id,
            request_message=request.request_message,
            created_at=request.created_at,
            from_user=UserDisplay.model_validate(request.sent_by)
        )

    model_config = config

    from_user: UserDisplay

class SentRequestPublic(FriendRequestBase):
    @classmethod
    def from_sent_request(cls, request: FriendRequest) -> "SentRequestPublic":
        return cls(
            id=request.id,
            request_message=request.request_message,
            created_at=request.created_at,
            to_user=UserDisplay.model_validate(request.received_by)
        )

    model_config = config

    to_user: UserDisplay

class FriendRequestUsersPublic(SQLModel):
    received: List[ReceivedRequestPublic]
    sent: List[SentRequestPublic] 