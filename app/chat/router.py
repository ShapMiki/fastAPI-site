from fastapi import APIRouter, WebSocket

from chats.service import manager

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


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
