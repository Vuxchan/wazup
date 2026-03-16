from fastapi import APIRouter
from src.api.routes import auth, user, friend, message, conversation

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(friend.router)
api_router.include_router(message.router)
api_router.include_router(conversation.router)