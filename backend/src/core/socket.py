import socketio
from src.api.deps import get_session, get_current_user
from src import crud
from src.schemas import ConversationUpdate, ReadMessageUpdate, ConversationPublic
from uuid import UUID

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

sio_app = socketio.ASGIApp(
    socketio_server=sio,
    socketio_path="socket.io"
)

user_to_sids = {}
sid_to_user = {}

@sio.event
async def connect(sid, environ, auth) -> None:
    token = auth.get('token')
    session = next(get_session())
    user = get_current_user(session, token)

    print(f'{user.username} connected to socket with id {sid}')

    user_id = user.id
    sid_to_user[sid] = user_id

    if user_id not in user_to_sids:
        user_to_sids[user_id] = set()

    user_to_sids[user_id].add(sid)

    online_users = [str(uid) for uid in user_to_sids.keys()]
    await sio.emit("online_users", online_users)

    conversation_ids = crud.get_conversation_ids(session, user_id)
    for cid in conversation_ids:
        await sio.enter_room(sid, cid)

    await sio.enter_room(sid, str(user_id))

@sio.event
async def disconnect(sid) -> None:
    user_id = sid_to_user[sid]

    if user_id:
        user_to_sids[user_id].discard(sid)

        if not user_to_sids[user_id]:
            del user_to_sids[user_id]

        del sid_to_user[sid]

    online_users = [str(uid) for uid in user_to_sids.keys()]
    await sio.emit("online_users", online_users)

    print(f'{sid} disconnected')

async def emit_new_message(conversation_update: ConversationUpdate):
    data = conversation_update.model_dump(mode="json", by_alias=True)
    await sio.emit("new_message", data, str(conversation_update.conversation.id))

async def emit_read_message(conversation_update: ReadMessageUpdate):
    data = conversation_update.model_dump(mode="json", by_alias=True)
    await sio.emit("read_message", data, str(conversation_update.conversation.id))

async def emit_new_group(conversation: ConversationPublic, user_id: UUID):
    data = conversation.model_dump(mode="json", by_alias=True)
    await sio.emit("new_group", data, str(user_id))

@sio.on("join_conversation")
async def join_conversation(sid, conversation_id):
    await sio.enter_room(sid, conversation_id)