from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from sqlalchemy import DateTime
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4, 
        primary_key=True
    )

    hashed_password: str = Field(
        nullable=False,
        min_length=8,
        max_length=128
    )

    email: str = Field(
        nullable=False,
        unique=True,
        index=True,
        max_length=255
    )

    username: str = Field(
        nullable=False,
        unique=True,
        index=True,
        max_length=50
    )

    displayed_name: str = Field(
        default=None,
        max_length=100,
        nullable=False
    )

    avatar_url: Optional[str] = Field(
        default=None,
        max_length=500
    )

    avatar_id: Optional[str] = Field(
        default=None,
        max_length=100
    )

    bio: Optional[str] = Field(
        default=None,
        max_length=500
    )

    phone: Optional[str] = Field(
        default=None,
        max_length=20
    )

    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),  
    )

    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),  
    )