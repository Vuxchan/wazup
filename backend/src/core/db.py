from sqlmodel import Session, create_engine, select, text
from src.core.config import settings
from src.models.user import User

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))