from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

import models
from .connections import UserConnect, connections
import services

game = services.Game(connections.find, connections.notify)

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
        await user.data.processing()
        await user.data.save()
        send_data = await models.UserDataPydanic.from_tortoise_orm(user.data)

        await connections.add(UserConnect(user, websocket))
        await connections.notify(user.id, {'type': 'sync', 'data': send_data.dict()})
    
    async def on_receive(self, websocket: WebSocket, data: dict):
        user_connect = connections.find(websocket.user_id)
        if not user_connect:
            return

        if "action" in data:
            await game.action(websocket.user_id, data)

    async def on_disconnect(self, websocket: WebSocket, close_code):
        if hasattr(websocket, 'user_id'):
            await connections.remove(websocket.user_id)
    
