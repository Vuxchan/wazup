from sqlmodel import SQLModel, Field, DateTime, Relationship, Index, desc
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .user import User
    from .conversation import Conversation

class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"

class Message(SQLModel, table=True):
    __table_args__ = (
        Index("idx_message_conversation_created_desc", "conversation_id", desc("created_at")),
    )

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    conversation_id: UUID = Field(
        foreign_key="conversation.id",
        index=True
    )

    sender_id: UUID = Field(foreign_key="user.id")

    type: MessageType = Field(default=MessageType.TEXT)

    content: Optional[str] = None

    img_url: Optional[str] = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),  
    )

    # Relationships
    conversation: "Conversation" = Relationship(
        back_populates="messages",
        sa_relationship_kwargs={
            "foreign_keys": "[Message.conversation_id]"
        }
    )
    sender: "User" = Relationship()