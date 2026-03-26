from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from src.utils import config

#Request models
class UserCreate(SQLModel):
    model_config = config

    username: str
    password: str
    email: str
    first_name: str
    last_name: str

#Response models
class UserPublic(SQLModel):
    model_config = config

    id: UUID
    email: str
    username: str
    display_name: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    phone: Optional[str]
    created_at: datetime

class UserDisplay(SQLModel):
    model_config = config

    id: UUID
    username: str
    display_name: Optional[str]
    avatar_url: Optional[str]