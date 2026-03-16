from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional

class MessageCreate(SQLModel):
    content: str
    conversation_id: UUID

class DirectMessageCreate(SQLModel):
    recipient_id: UUID
    content: str

class GroupMessageCreate(SQLModel):
    conversation_id: UUID
    content: str

class MessagePublic(SQLModel):
    id: UUID
    sender_id: UUID
    conversation_id: UUID
    content: str
    created_at: datetime

class MessagePagePublic(SQLModel):
    messages: List[MessagePublic]
    cursor: Optional[str]