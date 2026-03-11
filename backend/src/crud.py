from sqlmodel import Session, select
from src.models.user import User
from src.schemas.user import UserCreate
from src.core.security import Hasher
from datetime import timedelta, datetime, timezone
from src.models.sessions import Sessions
from uuid import UUID
from hashlib import sha256

DUMMY_HASH = "$2b$12$YLLg/ZlJqYLAANUOXuT3OuxYGMXtqgAUNohYmD5BzUJKH7gPpo7Fm"

def get_user_by_email(session: Session, email: str) -> User:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user

def get_user_by_username(session: Session, username: str) -> User:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user

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