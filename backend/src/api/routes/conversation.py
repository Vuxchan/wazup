from fastapi import APIRouter, HTTPException, status
from src.api.deps import SessionDep, CurrentUser
from src.models import Conversation, ConversationType
from src.schemas import ConversationCreate, BaseConversationPublic, MessagePagePublic, ConversationsResponse, ReadMessageUpdate
from src import crud
from typing import Optional
from uuid import UUID
from src.core.socket import emit_read_message

router = APIRouter(tags=["conversation"], prefix="/conversations")

@router.post("", status_code=status.HTTP_201_CREATED)
def create_conversation(session: SessionDep, current_user: CurrentUser, data: ConversationCreate) -> Conversation:
    type = data.type
    name = data.name
    member_ids = data.member_ids
    user_id = current_user.id

    not_friend_ids = crud.check_friendships(session, user_id, member_ids)
    if len(not_friend_ids) != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Can only add friends to your group {not_friend_ids}")

    conversation = None
    match type:
        case ConversationType.DIRECT:
            if len(member_ids) != 1:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Direct conversation must have exactly 1 member")

            participant_id = member_ids[0]

            conversation = crud.get_direct_conversation(session, user_id, participant_id)

            if not conversation:
                conversation = crud.create_direct_conversation(session, user_id, participant_id)

        case ConversationType.GROUP:
            if not name or len(member_ids) < 2:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Group name and member list are required")
            conversation = crud.create_group_conversation(session, [user_id] + member_ids, name)

    return conversation

@router.get("", status_code=status.HTTP_200_OK)
def get_conversations(session: SessionDep, current_user: CurrentUser) -> ConversationsResponse:
    user_id = current_user.id
    conversations = crud.get_all_conversations(session, user_id)
    base_conversations = [BaseConversationPublic.from_base_conversation(c) for c in conversations]
    return ConversationsResponse(
        conversations=base_conversations
    )

@router.get("/{conversation_id}/messages", status_code=status.HTTP_200_OK)
def get_messages(session: SessionDep, current_user: CurrentUser, conversation_id: UUID, size: int = 50, cursor: Optional[str] = None) -> MessagePagePublic:
    user_id = current_user.id

    conversation = crud.get_conversation_by_id(session, conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    
    if not next(filter(lambda p: p.user_id == user_id, conversation.participants), False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a conversation member")

    page = crud.paginate_messages(session, conversation_id, size, cursor)
    return MessagePagePublic(
        messages=page.items[::-1],
        cursor=page.next_page
    )

@router.patch("/{conversation_id}/seen")
async def mark_as_seen(session: SessionDep, current_user: CurrentUser, conversation_id: UUID) -> None:
    user_id = current_user.id

    conversation = crud.get_conversation_by_id(session, conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    
    last_message = conversation.last_message
    if not last_message:
        return
    
    if last_message.sender_id == str(user_id):
        return
    
    participant = next(filter(lambda p: p.user_id == user_id, conversation.participants))
    crud.upd_unread_count(session, participant)

    await emit_read_message(ReadMessageUpdate.from_read_message_update(conversation, user_id))