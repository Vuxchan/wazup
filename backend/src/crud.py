from sqlmodel import Session, select, and_, or_
from sqlalchemy.orm import selectinload
from src.models.user import User
from src.models.friendship import Friendship
from src.models.friend_request import FriendRequest
from src.schemas.user import UserCreate
from src.schemas.friend import Invitation
from src.core.security import Hasher
from datetime import timedelta, datetime, timezone
from src.models.sessions import Sessions
from uuid import UUID
from hashlib import sha256
from typing import Optional, List

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

def create_friend_request(session: Session, from_user: UUID, invitation: Invitation) -> FriendRequest:
    friend_request = FriendRequest(
        from_user_id=from_user,
        to_user_id=invitation.to,
        request_message=invitation.request_message
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

def authenticate(session: Session, email: str, password: str) -> User | None:
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
            'displayed_name': f"{user_create.first_name} {user_create.last_name}"
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