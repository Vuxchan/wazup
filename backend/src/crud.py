from sqlmodel import Session, select, and_, or_, func
from sqlalchemy.orm import selectinload
from src.models.user import User
from src.models.friendship import Friendship
from src.models.friend_request import FriendRequest
from src.models.conversation import Conversation, ConversationType
from src.models.conversation_participant import ConversationParticipant
from src.models.message import Message
from src.models import ConversationGroup, Role
from src.schemas import MessagePublic
from src.schemas.user import UserCreate
from src.schemas.friend import FriendRequestCreate, FriendRequestFilter
from src.core.security import Hasher
from datetime import timedelta, datetime, timezone
from src.models.sessions import Sessions
from uuid import UUID
from hashlib import sha256
from typing import Optional, List
from fastapi_pagination import set_params, set_page
from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.ext.sqlalchemy import paginate

DUMMY_HASH = "$2b$12$YLLg/ZlJqYLAANUOXuT3OuxYGMXtqgAUNohYmD5BzUJKH7gPpo7Fm"

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user

def get_user_by_username(session: Session, username: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user

def get_user_by_id(session: Session, id: UUID) -> Optional[User]:
    statement = select(User).where(User.id == id)
    user = session.exec(statement).first()
    return user

def check_friendship(session: Session, user1: UUID, user2: UUID) -> bool:
    statement = select(Friendship).where(
        or_(
            and_(Friendship.user_id == user1, Friendship.friend_id == user2),
            and_(Friendship.user_id == user2, Friendship.friend_id == user1)
        )
    )
    result = session.exec(statement).first()
    return result is not None

def check_friend_request(session: Session, user1: UUID, user2: UUID) -> bool:
    statement = select(FriendRequest).where(
        or_(
            and_(FriendRequest.from_user_id == user1, FriendRequest.to_user_id == user2),
            and_(FriendRequest.from_user_id == user2, FriendRequest.to_user_id == user1)
        )
    )
    result = session.exec(statement).first()
    return result is not None

def create_friend_request(session: Session, from_user: UUID, FriendRequestCreate: FriendRequestCreate) -> FriendRequest:
    friend_request = FriendRequest(
        from_user_id=from_user,
        to_user_id=FriendRequestCreate.to,
        request_message=FriendRequestCreate.request_message
    )
    session.add(friend_request)
    session.commit()
    session.refresh(friend_request)
    return friend_request

def get_request_by_id(session: Session, request_id: UUID) -> Optional[FriendRequest]:
    statement = select(FriendRequest).where(FriendRequest.id == request_id)
    friend_request = session.exec(statement).first()
    return friend_request

def create_friendship(session: Session, friend_request: FriendRequest) -> Friendship:
    friendship = Friendship(
        user_id=friend_request.from_user_id,
        friend_id=friend_request.to_user_id
    )
    session.add(friendship)
    session.delete(friend_request)
    session.commit()
    session.refresh(friendship)
    return friendship

def delete_friend_req(session: Session, friend_request: FriendRequest) -> None:
    session.delete(friend_request)
    session.commit()

def get_all_friendships(session: Session, user_id: UUID) -> List[Friendship]:
    statement = select(Friendship).options(
        selectinload(Friendship.user_A), 
        selectinload(Friendship.user_B)
    ).where(or_(Friendship.user_id == user_id, Friendship.friend_id == user_id))
    friendships = session.exec(statement).all()
    return friendships

def get_all_requests(session: Session, user_id: UUID) -> FriendRequestFilter:
    statement = select(FriendRequest).options(
        selectinload(FriendRequest.sent_by),
        selectinload(FriendRequest.received_by)
    ).where(or_(FriendRequest.to_user_id == user_id, FriendRequest.from_user_id == user_id))
    requests = session.exec(statement).all()

    sent = []
    received = []
    list(map(lambda r: received.append(r) if r.to_user_id == user_id else sent.append(r), requests))
    return FriendRequestFilter(received=received, sent=sent)

def authenticate(session: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(session, email)
    if not user:
        Hasher.verify_password(password, DUMMY_HASH)
        return None
    if not Hasher.verify_password(password, user.hashed_password):
        return None
    return user

def delete_session_by_token(session: Session, token: str) -> None:
    user_session = get_session_by_token(session, token)
    if user_session:
        session.delete(user_session)
        session.commit()

def create_user(session: Session, user_create: UserCreate) -> User:
    user = User.model_validate(
        user_create, 
        update={
            'hashed_password': Hasher.get_password_hash(user_create.password),
            'display_name': f"{user_create.last_name} {user_create.first_name}"
            }
        )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def create_refresh_token(session: Session, user_id: UUID, refresh_token: str, expires_delta: timedelta) -> None:
    expire = datetime.now(timezone.utc) + expires_delta
    user_session = Sessions(refresh_token=sha256(refresh_token.encode()).hexdigest(), expires_at=expire, user_id=user_id)
    session.add(user_session)
    session.commit()
    session.refresh(user_session)

def get_session_by_token(session: Session, token: str) -> Sessions:
    token_hash = sha256(token.encode()).hexdigest()
    statement = select(Sessions).where(Sessions.refresh_token == token_hash)
    user_session = session.exec(statement).first()
    return user_session 

def get_conversation_by_id(session: Session, conversation_id: UUID) -> Conversation:
    statement = select(Conversation).options(selectinload(Conversation.participants)).where(Conversation.id == conversation_id)
    conversation = session.exec(statement).first()
    return conversation

def create_participant(conversation_id: UUID, user_id: UUID) -> ConversationParticipant:
    participant = ConversationParticipant(
        conversation_id=conversation_id,
        user_id=user_id
    )
    return participant

def create_direct_conversation(session: Session, sender_id: UUID, recipient_id: UUID) -> Conversation:
    # conversation = Conversation(last_message_at=datetime.now(timezone.utc))
    conversation = Conversation()
    session.add(conversation)
    session.flush()

    sender = create_participant(conversation.id, sender_id)
    recipient = create_participant(conversation.id, recipient_id)

    session.add_all([sender, recipient])
    session.commit()
    session.refresh(conversation)
    return conversation

def create_message(session: Session, conversation_id: UUID, sender_id: UUID, content: str) -> Message:
    message = Message(
        conversation_id=conversation_id,
        sender_id=sender_id,
        content=content
    )
    session.add(message)
    session.flush()
    session.refresh(message)
    return message

def upd_conv_after_create_msg(session: Session, conversation: Conversation, message: Message) -> None:
    conversation.last_message_at = message.created_at
    conversation.last_message_id = message.id

    for member in conversation.participants:
        if member.user_id == message.sender_id:
            member.unread_count = 0
            member.last_read_message_id = message.id
        else:
            member.unread_count += 1
    session.commit()

def get_direct_conversation(session: Session, sender_id: UUID, recipient_id: UUID) -> Optional[Conversation]:
    statement = (
        select(Conversation)
        .options(selectinload(Conversation.participants))
        .join(ConversationParticipant)
        .where(Conversation.type == ConversationType.DIRECT, ConversationParticipant.user_id.in_([sender_id, recipient_id]))
        .group_by(Conversation.id)
        .having(func.count(ConversationParticipant.user_id) == 2)
    )
    conversation = session.exec(statement).first()
    return conversation

def create_group_conversation(session: Session, member_ids: List[UUID], name: str) -> Conversation:
    # conversation = Conversation(last_message_at=datetime.now(timezone.utc))
    conversation = Conversation(type=ConversationType.GROUP)
    session.add(conversation)
    session.flush()

    participant = [create_participant(conversation.id, m) for m in member_ids]
    participant[0].role = Role.HOST
    session.add_all(participant)

    group = ConversationGroup(
        conversation_id=conversation.id,
        created_by=member_ids[0],
        name=name
    )
    session.add(group)

    session.commit()
    session.refresh(conversation)

    return conversation

def get_all_conversations(session: Session, user_id: UUID) -> List[Conversation]:
    statement = (
        select(Conversation)
        .options(selectinload(Conversation.participants).selectinload(ConversationParticipant.user))
        .options(selectinload(Conversation.last_message).selectinload(Message.sender))
        .options(selectinload(Conversation.group))
        .join(ConversationParticipant)
        .where(ConversationParticipant.user_id == user_id)
        .order_by(Conversation.last_message_at.desc())
    )
    conversations = session.exec(statement).all()   
    return conversations

def paginate_messages(session: Session, conversation_id: UUID, size: int, cursor: Optional[str]) -> CursorPage[MessagePublic]:
    set_page(CursorPage[Message])
    set_params(CursorParams(size=size, cursor=cursor))

    page = paginate(session, select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.desc(), Message.id.desc()))
    page.items = [MessagePublic.model_validate(m) for m in page.items]
    return page

def check_friendships(session: Session, user_id: UUID, friend_ids: List[UUID]) -> List[UUID]:
    friend_ids = set(friend_ids)

    statement = (
        select(Friendship.friend_id)
        .where(
            Friendship.user_id == user_id,
            Friendship.friend_id.in_(friend_ids)
        )
    )

    friends = set(session.exec(statement).all())
    invalid_friends = friend_ids - friends
    return invalid_friends