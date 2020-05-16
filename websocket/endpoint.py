from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

import models
from .connections import UserConnect, connections

class EndPoint(WebSocketEndpoint):
    encoding = "json"

    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()
        if not 'token' in self.scope['path_params']:
            await websocket.close()
            return
        
        user = await models.User.filter(token=self.scope['path_params']['token']).prefetch_related('data').get_or_none()
        if not user:
            await websocket.close()
            return

        websocket.user_id = user.id
        await connections.add(UserConnect(user, websocket))
        

    async def on_receive(self, websocket: WebSocket, data: dict):
        await websocket.send_json(data)

    async def on_disconnect(self, websocket: WebSocket, close_code):
        if hasattr(websocket, 'user_id'):
            await connections.remove(websocket.user_id)
    
