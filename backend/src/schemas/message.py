from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from src.utils import config

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