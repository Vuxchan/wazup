from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlalchemy import DateTime

class Sessions(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    user_id: UUID = Field(
        foreign_key="user.id"
    )

    refresh_token: str

    expires_at: datetime = Field(sa_type=DateTime(timezone=True))

    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),  
    )

    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),  
    )

    revoked: bool = False