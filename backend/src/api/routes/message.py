from fastapi import APIRouter, HTTPException, status
from src.api.deps import SessionDep, CurrentUser
from typing import Any
from src.schemas import DirectMessageCreate, MessagePublic, GroupMessageCreate, ConversationUpdate
from src import crud
from src.core.socket import emit_new_message
from sqlmodel import inspect

router = APIRouter(tags=["message"], prefix="/messages")

@router.post("/direct", status_code=status.HTTP_201_CREATED, response_model=MessagePublic)
async def send_direct_message(session: SessionDep, current_user: CurrentUser, data: DirectMessageCreate) -> Any:
    sender_id = current_user.id
    recipient_id = data.recipient_id
    content= data.content

    if sender_id == recipient_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't message yourself")

    if len(crud.check_friendships(session, sender_id, [recipient_id])) != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not friend of each other {recipient_id}")

    if not content or not content.strip():
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No message content")

    conversation = crud.get_direct_conversation(session, sender_id, recipient_id)

    if not conversation:
        conversation = crud.create_direct_conversation(session, sender_id, recipient_id)

    message = crud.create_message(session, conversation, sender_id, content, data.img_url)

    crud.upd_conv_after_create_msg(session, conversation, message)

    await emit_new_message(ConversationUpdate.from_conversation_update(message, current_user, conversation))

    return message

@router.post("/group", status_code=status.HTTP_201_CREATED, response_model=MessagePublic)
async def send_group_message(session: SessionDep, current_user: CurrentUser, data: GroupMessageCreate) -> Any:
    sender_id = current_user.id
    content = data.content
    conversation_id = data.conversation_id

    conversation = crud.get_conversation_by_id(session, conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    
    if not next(filter(lambda p: p.user_id == sender_id, conversation.participants), False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a conversation member")
    
    if not content or not content.strip():
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No message content")
    
    message = crud.create_message(session, conversation_id, sender_id, content, data.img_url)

    crud.upd_conv_after_create_msg(session, conversation, message)

    await emit_new_message(ConversationUpdate.from_conversation_update(message, current_user, conversation))

    return message