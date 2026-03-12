from sqlmodel import SQLModel, Field, DateTime, UniqueConstraint, CheckConstraint
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional

class FriendRequest(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("from_user_id", "to_user_id"),
    )

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    from_user_id: UUID = Field(
        foreign_key="user.id",
        index=True
    )

    to_user_id: UUID = Field(
        foreign_key="user.id",
        index=True
    )

    request_message: Optional[str] = Field(
        default=None,
        max_length=300
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),  
    )