from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from src.utils import config
from .user import LastMessageSenderPublic
from src.models import User

class BaseMessage(SQLModel):
    content: str
    img_url: Optional[str] = None

class DirectMessageCreate(BaseMessage):
    model_config = config

    recipient_id: UUID

class GroupMessageCreate(BaseMessage):
    model_config = config

    conversation_id: UUID

class MessagePublic(BaseMessage):
    model_config = config

    id: UUID
    sender_id: UUID
    conversation_id: UUID
    created_at: datetime

class MessagePagination(SQLModel):
    messages: List[MessagePublic]
    cursor: Optional[str]

class Message(SQLModel):
    message: str

class LastMessageDisplay(SQLModel):
    model_config = config

    content: Optional[str] = None
    created_at: Optional[datetime] = None

class LastMessagePublic(SQLModel):
    @classmethod
    def from_last_message(cls, last_message: Message, sender: User) -> "LastMessagePublic":
        return cls(
            id=last_message.id,
            content=last_message.content,
            created_at=last_message.created_at,
            sender=LastMessageSenderPublic.from_last_message_sender(sender)
        )
    
    model_config = config

    id: UUID
    content: str
    created_at: datetime
    sender: LastMessageSenderPublic