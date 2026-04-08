from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from src.utils import config
from src.models import User

#Request models
class UserCreate(SQLModel):
    model_config = config

    username: str
    password: str
    email: str
    first_name: str
    last_name: str

#Response models
class UserPublic(SQLModel):
    model_config = config

    id: UUID
    email: str
    username: str
    display_name: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    phone: Optional[str]
    created_at: datetime

class UserDisplay(SQLModel):
    model_config = config

    id: UUID
    username: str
    display_name: Optional[str]
    avatar_url: Optional[str] = None

class LastMessageSenderPublic(UserDisplay):
    @classmethod
    def from_last_message_sender(cls, sender: User) -> "LastMessageSenderPublic":
        return cls(
            id=sender.id,
            display_name=sender.display_name,
            avatar_url=sender.avatar_url,
            username=sender.username
        )
    
    model_config = config