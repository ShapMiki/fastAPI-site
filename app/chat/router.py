from fastapi import APIRouter, WebSocket, Depends, HTTPException
#e
from users.schemas import SUser, SUserLogin, SUser_personal_info
from users.dependencies import get_current_user
from users.dao import UsersDAO

from exceptions import *

from chat.dao import ChatDAO, MessageDAO
from chat.service import *
from chat.schemas import *

from exceptions import NotFound

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

@router.post("/create_chat_api/{user_id}")
async def create_chat_api(user_id: int, user: SUser = Depends(get_current_user)):
    second_user = await UsersDAO.find_one_or_none(id=user_id)
    if user and second_user:
        await ChatDAO.create_chat(user, second_user )
    else:
        return NotFound


@router.post("/send_message_api/{chat_id}")
async def send_message_api(chat_id, message : SMessage, user: SUser = Depends(get_current_user)):
    chat_id = int(chat_id)
    message = message.message
    if not message:
        raise HTTPException(status_code=400, detail="Message is empty")
    if user:
        await send_message(user, chat_id, message)
    else:
        raise HTTPException(status_code=403)


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    print("OK")
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client {chat_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
