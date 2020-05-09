import uuid
import datetime
import re

from tortoise.transactions import atomic

from models import User, UserData, UserDataPydanic
from fastapi import HTTPException

class Users:
    def __init__(self):
        pass

    async def get_or_create_vk(self, vk_id) -> str: 
        user = await User.filter(vk_id=vk_id).get_or_none()

        if user:
            pass
            # update token
            # user.token = await self.gen_token()
            # user.save()
        else:
            user = await self._create_vk_user(vk_id)

        return user

    async def _create_vk_user(self, vk_id: int):
        token = await self.gen_token()
        user = await User.create(vk_id=vk_id, token=token)
        await UserData.create(user=user, time=int(datetime.datetime.utcnow().timestamp()))
        return user

    async def gen_token(self):
        return str(uuid.uuid4())
    
    @atomic()
    async def get_user_data(self, token):
        user_data = await UserData.filter(user__token=token).get_or_none()
        if not user_data:
            raise HTTPException(404, "Not found")
        await user_data.processing()
        await user_data.save()
        return await UserDataPydanic.from_tortoise_orm(user_data)
    
    async def set_nickname(self, token: str, nickname: str):
        if (len(nickname) < 3):
            raise HTTPException(400, 'Too short, min 3')
        if (len(nickname) > 18):
            raise HTTPException(400, 'Too long, max 18')
        print(not bool(re.compile(r'[^a-zA-Z0-9.\-\_\]\[]').search(nickname)))
        
        await User.filter(token=token).update(nickname=nickname)
        return nickname