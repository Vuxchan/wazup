from sqlmodel import SQLModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from src.models import ConversationType, ConversationParticipant, Message, Conversation

class ConversationCreate(SQLModel):
    member_ids: List[UUID]
    type: ConversationType
    name: Optional[str]

class ParticipantPublic(SQLModel):
    @classmethod
    def from_participant(cls, participant: ConversationParticipant) -> "ParticipantPublic":
        return cls(
            user_id=participant.user_id,
            displayed_name=participant.user.displayed_name,
            avatar_url=participant.user.avatar_url,
            joined_at=participant.joined_at
        )

    user_id: UUID
    displayed_name: str
    avatar_url: Optional[str] = None
    joined_at: datetime

class LastMessageSenderPublic(SQLModel):
    @classmethod
    def from_last_message_sender(cls, last_message: Message) -> "LastMessageSenderPublic":
        return cls(
            sender_id=last_message.sender_id,
            displayed_name=last_message.sender.displayed_name,
            avatar_url=last_message.sender.avatar_url,
            content=last_message.content
        )

    sender_id: UUID
    displayed_name: str
    avatar_url: Optional[str] = None
    content: str

class GroupConversationPublic(SQLModel):
    created_by: UUID
    group_name: str
    avatar_group_url: Optional[str] = None

class BaseConversationPublic(SQLModel):
    @classmethod
    def from_base_conversation(cls, conversation: Conversation) -> "BaseConversationPublic":
        return cls(
            id=conversation.id,
            type=conversation.type,
            last_message_at=conversation.last_message_at,
            last_message_id=conversation.last_message_id,
            created_at=conversation.created_at,
            participants=[ParticipantPublic.from_participant(p) for p in conversation.participants],
            last_message_sender=(
                LastMessageSenderPublic.from_last_message_sender(conversation.last_message)
                if conversation.last_message else None
            ),
            group=(
                GroupConversationPublic.model_validate(conversation.group)
                if conversation.type == ConversationType.GROUP and conversation.group else None
            )
        )

    id: UUID
    type: ConversationType
    last_message_at: Optional[datetime] = None
    last_message_id: Optional[UUID] = None
    created_at: datetime
    participants: List[ParticipantPublic]
    last_message_sender: Optional[LastMessageSenderPublic] = None
    group: Optional[GroupConversationPublic] = None