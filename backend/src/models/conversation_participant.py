from sqlmodel import SQLModel, Field, DateTime, Relationship, Index
from uuid import UUID
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .conversation import Conversation
    from .user import User
    from .message import Message

class Role(str, Enum):
    HOST = "host"
    MEMBER = "member"

class ConversationParticipant(SQLModel, table=True):
    __table_args__ = (
        Index("idx_user_conversations", "user_id", "conversation_id"),
        Index("idx_conv_participants", "conversation_id"),
    )

    conversation_id: UUID = Field(
        foreign_key="conversation.id",
        primary_key=True
    )

    user_id: UUID = Field(
        foreign_key="user.id",
        primary_key=True
    )

    role: Role = Field(default=Role.MEMBER)

    joined_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),  
    )

    unread_count: int = Field(default=0)

    last_read_message_id: Optional[UUID] = Field(
        default=None,
        foreign_key="message.id"
    )

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="participants")
    user: "User" = Relationship(back_populates="conversations")
    last_read_message: Optional["Message"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "ConversationParticipant.last_read_message_id"
        }
    )