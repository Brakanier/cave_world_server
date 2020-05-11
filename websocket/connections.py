from typing import List, Dict

from starlette.websockets import WebSocket, WebSocketDisconnect

class Connections:
    def __init__(self):
        self.websockets: Dict[int, WebSocket] = {}
    
    async def push(self, user_id: int, data: dict):
        self.websockets[user_id].send_json(data)
    
    async def connect(self, user_id: int, websocket: WebSocket):
        self.websockets[user_id] = websocket
    
    async def disconnect(self, user_id: int):
        if user_id in self.websockets:
            del self.websockets[user_id]