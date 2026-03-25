from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from src.utils import config

class MessageCreate(SQLModel):
    content: str
    conversation_id: UUID

class DirectMessageCreate(SQLModel):
    model_config = config

    recipient_id: UUID
    content: str
    img_url: Optional[str] = None

class GroupMessageCreate(SQLModel):
    model_config = config

    conversation_id: UUID
    content: str
    img_url: Optional[str] = None

class MessagePublic(SQLModel):
    model_config = config

    id: UUID
    sender_id: UUID
    conversation_id: UUID
    content: str
    created_at: datetime
    img_url: Optional[str]

class MessagePagePublic(SQLModel):
    messages: List[MessagePublic]
    cursor: Optional[str]

class Message(SQLModel):
    message: str