from sqlmodel import SQLModel
from uuid import UUID
from typing import Optional

class Invitation(SQLModel):
    to: UUID
    request_message: Optional[str]