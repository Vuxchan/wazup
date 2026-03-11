from src.utils import config
from sqlmodel import SQLModel

class Token(SQLModel):
    # model_config=config

    access_token: str 
    token_type: str = "bearer"

class TokenPayload(SQLModel):
    sub: str | None = None