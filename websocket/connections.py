from typing import List, Dict

import asyncio
from starlette.websockets import WebSocket, WebSocketDisconnect
import time
import models

class UserConnect():
    def __init__(self, user: models.User, websocket: WebSocket):
        self.user = user
        self.websocket = websocket

    async def send(self, data: dict):
        await self.websocket.send_json(data)


async def connections_process(connections, notify) -> None:
    while True:
        print(len(connections))
        for user_id in connections:
            data = connections[user_id].user.data
            await data.processing()
            await data.save()
            send_data = await models.UserDataPydanic.from_tortoise_orm(data)
            await notify(user_id, send_data.dict())
        await asyncio.sleep(10)


class Connections:
    def __init__(self):
        self.__connections: Dict[int, UserConnect] = {}
        asyncio.ensure_future(connections_process(self.__connections, self.notify))
    
    def find(self, user_id):
        if user_id in self.__connections:
            return self.__connections[user_id]
        else:
            return None

    async def notify(self, user_id, data):
        if user_id in self.__connections:
            await self.__connections[user_id].send(data)

    async def add(self, user_connect: UserConnect):
        self.__connections[user_connect.user.id] = user_connect
    
    async def remove(self, user_id: int):
        if user_id in self.__connections:
            del self.__connections[user_id]

    def __len__(self):
        return len(self.__connections)


connections = Connections()


