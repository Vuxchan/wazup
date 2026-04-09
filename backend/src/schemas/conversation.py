from sqlmodel import SQLModel
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from src.models import ConversationType, ConversationParticipant, Message, Conversation, User
from src.utils import config
from .message import LastMessagePublic, MessagePublic, LastMessageDisplay
from .user import UserDisplay

class ConversationCreate(SQLModel):
    model_config = config

    member_ids: List[UUID]
    type: ConversationType
    name: Optional[str]

class ParticipantPublic(SQLModel):
    @classmethod
    def from_participant(cls, participant: ConversationParticipant) -> "ParticipantPublic":
        return cls(
            id=participant.user_id,
            display_name=participant.user.display_name,
            avatar_url=participant.user.avatar_url,
            username=participant.user.username,
            joined_at=participant.joined_at
        )
    
    @classmethod
    def first_create(cls, user: User) -> "ParticipantPublic":
        return cls(
            id=user.id,
            display_name=user.display_name,
            avatar_url=user.avatar_url,
            username=user.username
        )
    
    model_config = config

    id: UUID
    display_name: str
    avatar_url: Optional[str] = None
    username: str
    joined_at: Optional[datetime] = None

class GroupConversationPublic(SQLModel):
    model_config = config

    created_by: UUID
    name: str
    # avatar_group_url: Optional[str] = None

class ConversationDisplay(SQLModel):
    @classmethod
    def from_conversation_display(cls, row: Any) -> "ConversationDisplay":
        return cls(
            id=row.conversation_id,
            last_message=LastMessageDisplay(content=row.content, created_at=row.created_at, id=row.last_message_id) if row.last_message_id else None,
        )

    model_config = config

    id: UUID
    last_message: Optional[LastMessageDisplay]
    unread_counts: Dict[UUID, int] = {}
    participants: List[UserDisplay] = []
    type: ConversationType = "direct"
    group: Optional[GroupConversationPublic] = None

class ConversationPublic(SQLModel):
    @classmethod
    def from_conversation(cls, conversation: Conversation) -> "ConversationPublic":
        return cls(
            id=conversation.id,
            type=conversation.type,
            last_message_at=conversation.last_message_at,
            last_message_id=conversation.last_message_id,
            created_at=conversation.created_at,
            participants=[ParticipantPublic.from_participant(p) for p in conversation.participants],
            last_message=(
                LastMessagePublic.from_last_message(conversation.last_message, conversation.last_message.sender)
                if conversation.last_message else None
            ),
            group=(
                GroupConversationPublic.model_validate(conversation.group)
                if conversation.type == ConversationType.GROUP and conversation.group else None
            ),
            unread_counts={
                p.user_id: p.unread_count
                for p in conversation.participants
            },
            seen_by= [p.user_id for p in conversation.participants if p.unread_count == 0 and p.user_id != conversation.last_message.sender_id] if conversation.last_message else []
        )
    
    @classmethod
    def first_create(cls, conversation: Conversation, users: List[User]) -> "ConversationPublic":
        return cls(
            id=conversation.id,
            type=conversation.type,
            created_at=conversation.created_at,
            participants=[ParticipantPublic.first_create(user) for user in users],
            unread_counts={},
            seen_by=[]
        )
    
    model_config = config
    
    id: UUID
    type: ConversationType
    last_message_at: Optional[datetime] = None
    last_message_id: Optional[UUID] = None
    created_at: datetime
    participants: List[ParticipantPublic]
    last_message: Optional[LastMessagePublic] = None
    group: Optional[GroupConversationPublic] = None
    unread_counts: Dict[UUID, int]
    seen_by: List[UUID]

class FetchMessagesResponse(SQLModel):
    model_config = config

    participants_last_read_message: Dict[UUID, Optional[datetime]] = {}
    seen_by: List[UUID] = []
    messages: List[MessagePublic]
    cursor: Optional[str]

class NewMessageUpdate(SQLModel):
    @classmethod
    def from_conversation_update(cls, last_message: Message, sender: User) -> "NewMessageUpdate":
        return cls(
            id=last_message.conversation_id,
            last_message=LastMessagePublic.from_last_message(last_message, sender),
            last_message_at=last_message.created_at
        )
    
    model_config = config

    id: UUID
    seen_by: List[UUID] = []
    last_message: LastMessagePublic
    last_message_at: datetime

class ReadMessageUpdate(SQLModel):
    @classmethod
    def from_read_message_update(cls, conversation_id: UUID, recipient_id: UUID) -> "ReadMessageUpdate":
        return cls(
            id=conversation_id,
            seen_by=[recipient_id]
        )

    model_config = config

    id: UUID
    seen_by: List[UUID]