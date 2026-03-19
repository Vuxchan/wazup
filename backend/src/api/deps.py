from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from collections.abc import Generator
from src.core.db import engine
from typing import Annotated
from src.models.user import User
from fastapi.security import OAuth2PasswordBearer
from src.core.config import settings
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from src.core import security
from src.schemas.token import TokenPayload

get_token = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/signin"
)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(get_token)]

def get_current_user(session: Session, token: str) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials",)
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def user_dep(session: SessionDep, token: TokenDep):
    return get_current_user(session, token)

CurrentUser = Annotated[User, Depends(user_dep)]