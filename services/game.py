import datetime

from tortoise.expressions import F
from tortoise.transactions import atomic

from models import User, UserData, UserDataPydanic
from .builds import Builds
from .citizens import Citizens

class Game:
    def __init__(self):
        self.build = Builds()
        self.citizen = Citizens()
    
    @atomic()
    async def action(self, token: str, action: str, amount=None):
        user_data = await UserData.filter(user__token=token).get()
        await user_data.processing()

        if action == 'wood':
            await self.extract(user_data, 'wood')
        elif action == 'stone':
            await self.extract(user_data, 'stone')
        elif action == 'wood_store':
            await self.build.wood_store(user_data)
        elif action == 'hut':
            await self.build.hut(user_data)
        elif action == 'wood_work':
            await self.build.wood_work(user_data)
        elif action == 'wood_inwork':
            await self.citizen.wood_inwork(user_data, amount) 


        await user_data.save()

        return await UserDataPydanic.from_tortoise_orm(user_data)

    async def extract(self, user_data, target):
        if user_data.energy < 1:
            return None
            
        if getattr(user_data, target) >= getattr(user_data, f'{target}_max')():
            return None

        user_data.energy -= 1

        setattr(user_data, target, getattr(user_data, target) + 1)


    


        
        
