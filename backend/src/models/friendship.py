from sqlmodel import SQLModel, Field, DateTime, UniqueConstraint
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import model_validator
from typing import Self

class Friendship(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "friend_id"),
    )

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    user_id: UUID = Field(foreign_key="user.id")

    friend_id: UUID = Field(foreign_key="user.id")

    @model_validator(mode="after")
    def standardlize_friendship(self) -> Self:
        if self.user_id > self.friend_id:
            self.user_id, self.friend_id = self.friend_id, self.user_id
        return self

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),  
    )