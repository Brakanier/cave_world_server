from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

class Connector(WebSocketEndpoint):
    encoding = "json"

    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()
        websocket.user_id =

    async def on_receive(self, websocket: WebSocket, data: dict):
        await websocket.send_bytes(b"Message: " + data)

    async def on_disconnect(self, websocket: WebSocket, close_code):
        pass
    
