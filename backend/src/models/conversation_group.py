from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .conversation import Conversation

class ConversationGroup(SQLModel, table=True):
    conversation_id: UUID = Field(
        foreign_key="conversation.id",
        primary_key=True
    )

    created_by: UUID = Field(
        foreign_key="user.id",
        index=True,
        nullable=True
    )

    name: Optional[str] = None

    avatar_group_url: Optional[str] = None

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="group")