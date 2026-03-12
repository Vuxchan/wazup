from sqlmodel import SQLModel, Field, DateTime, Relationship, Index
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .message import Message
    from .conversation_participant import ConversationParticipant

class ConversationType(str, Enum):
    DIRECT = "direct"
    GROUP = "group"

class Conversation(SQLModel, table=True):
    __table_args__ = (
        Index("idx_conversation_last_message", "last_message_at"),
    )

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    type: ConversationType = Field(
        default=ConversationType.DIRECT,
        nullable=False
    )

    created_by: UUID = Field(
        foreign_key="user.id",
        index=True
    )

    last_message_id: Optional[UUID] = Field(
        default=None,
        foreign_key="message.id"
    )

    last_message_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True)
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),  
    )
    
    # Relationships
    messages: List["Message"] =  Relationship(back_populates="conversation")
    participants: List["ConversationParticipant"] = Relationship(back_populates="conversation")