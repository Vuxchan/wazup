from sqlmodel import Session, create_engine, select, text
from src.core.config import settings
from src.models.user import User

print(str(settings.SQLALCHEMY_DATABASE_URI))
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))