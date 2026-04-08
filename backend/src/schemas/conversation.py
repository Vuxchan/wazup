from sqlmodel import SQLModel
from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime
from src.models import ConversationType, ConversationParticipant, Message, Conversation, User
from src.utils import config
from .message import MessagePublic

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

class LastMessageSenderPublic(SQLModel):
    @classmethod
    def from_last_message_sender(cls, sender: User) -> "LastMessageSenderPublic":
        return cls(
            id=sender.id,
            display_name=sender.display_name,
            avatar_url=sender.avatar_url
        )
    
    model_config = config

    id: UUID
    display_name: str
    avatar_url: Optional[str] = None

class LastMessagePublic(SQLModel):
    @classmethod
    def from_last_message(cls, last_message: Message) -> "LastMessagePublic":
        return cls(
            id=last_message.id,
            content=last_message.content,
            created_at=last_message.created_at,
            sender=LastMessageSenderPublic.from_last_message_sender(last_message.sender)
        )
    
    model_config = config

    id: UUID
    content: str
    created_at: datetime
    sender: LastMessageSenderPublic

class GroupConversationPublic(SQLModel):
    model_config = config

    created_by: UUID
    name: str
    # avatar_group_url: Optional[str] = None

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
                LastMessagePublic.from_last_message(conversation.last_message)
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

class ConversationListPublic(SQLModel):
    conversations: List[ConversationPublic]

class ConversationUpdate(SQLModel):
    @classmethod
    def from_conversation_update(cls, last_message: Message) -> "ConversationUpdate":
        return cls(
            id=last_message.conversation_id,
            last_message=LastMessagePublic.from_last_message(last_message),
            last_message_at=last_message.created_at
        )

    model_config = config

    id: UUID
    last_message: LastMessagePublic
    last_message_at: datetime

class NewMessageUpdate(SQLModel):
    @classmethod
    def from_conversation_update(cls, message: Message, sender: User) -> "NewMessageUpdate":
        return cls(
            message=MessagePublic.model_validate(message),
            sender=sender,
            conversation=ConversationUpdate.from_conversation_update(message),
        )
    
    model_config = config

    message: MessagePublic
    conversation: ConversationUpdate
    sender: User

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