from typing import Dict, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws", tags=["WebSockets"])


class ConnectionManager:
    def __init__(self):
        # org_id -> list of active websockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, org_id: str):
        await websocket.accept()
        if org_id not in self.active_connections:
            self.active_connections[org_id] = []
        self.active_connections[org_id].append(websocket)

    def disconnect(self, websocket: WebSocket, org_id: str):
        if org_id in self.active_connections:
            if websocket in self.active_connections[org_id]:
                self.active_connections[org_id].remove(websocket)

    async def broadcast_to_org(self, org_id: str, message: dict):
        if org_id in self.active_connections:
            for connection in self.active_connections[org_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass


ws_manager = ConnectionManager()


@router.websocket("/{org_id}")
async def websocket_endpoint(websocket: WebSocket, org_id: str):
    await ws_manager.connect(websocket, org_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo or handle incoming client ping
            await websocket.send_json({"type": "PONG", "data": data})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, org_id)
