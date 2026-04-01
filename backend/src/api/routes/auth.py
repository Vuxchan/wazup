from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from src.api.deps import SessionDep
from src.schemas.user import UserCreate
from typing import Annotated
from src import crud
from src.core import security
from src.core.config import settings
from src.schemas.token import Token
from datetime import timedelta, datetime, timezone
from secrets import token_urlsafe

router = APIRouter(tags=["auth"], prefix="/auth")

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(session: SessionDep, data: UserCreate) -> None:
    attr = vars(data)
    for _, value in attr.items():
        if value is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough information")
        
    if crud.get_user_by_email(session, data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    if crud.get_user_by_username(session, data.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    
    crud.create_user(session, data)    

@router.post("/signin")
def signin(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response) -> Token:
    email = form_data.username
    password = form_data.password
    if not email or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough credentials")
    
    user = crud.authenticate(session, email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    refresh_token = token_urlsafe(32)
    crud.create_refresh_token(session, user.id, refresh_token, timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_TIME))
    response.set_cookie(
        key="refresh_token", 
        value=refresh_token, 
        max_age=settings.REFRESH_TOKEN_EXPIRE_TIME, 
        secure=True,
        httponly=True,
        samesite="lax"
    )

    return Token(
        access_token=security.create_access_token(user.id, access_token_expires)
    )

@router.post("/signout", status_code=status.HTTP_204_NO_CONTENT)
def signout(session: SessionDep, request: Request, response: Response) -> None:
    token = request.cookies.get("refresh_token")
    if token:
        crud.delete_session_by_token(session, token)
    response.delete_cookie(
        key="refresh_token", 
        secure=True, 
        httponly=True, 
        samesite="lax"
    )

@router.post("/refresh")
def refresh_token(session: SessionDep, request: Request) -> Token:
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expiration")
    user_session = crud.get_session_by_token(session, token)

    if not user_session:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

    if user_session.revoked:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token revoked")
    
    if user_session.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return Token(
        access_token=security.create_access_token(user_session.user_id, access_token_expires)
    )