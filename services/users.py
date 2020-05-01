import uuid

from models import User

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
            user = await self.create_vk_user(vk_id)

        return user



    async def create_vk_user(self, vk_id: int):
        token = await self.gen_token()
        return await User.create(vk_id=vk_id, token=token)



    async def gen_token(self):
        return str(uuid.uuid4())