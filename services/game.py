import datetime

from tortoise.expressions import F
from tortoise.transactions import atomic
from tortoise.query_utils import Q, Prefetch

from models import User, UserData, UserDataPydanic, Battle
from .builds import Builds
from .citizens import Citizens
from .war import War

class Game:
    def __init__(self):
        self.build = Builds()
        self.citizen = Citizens()
        self.war = War()
    
    @atomic()
    async def action(self, token: str, action: str, amount=None):
        user_data = await UserData.filter(user__token=token).get()
        await user_data.processing()

        if action == 'wood':
            await self.extract(user_data, 'wood')
        elif action == 'stone':
            await self.extract(user_data, 'stone')
        
        elif action == 'hut':
            await self.build.hut(user_data)
        elif action == 'house':
            await self.build.house(user_data)
        elif action == 'mansion':
            await self.build.mansion(user_data)

        elif action == 'wood_store':
            await self.build.wood_store(user_data)
        elif action == 'stone_store':
            await self.build.stone_store(user_data)
        
        elif action == 'wood_work':
            await self.build.wood_work(user_data)
        elif action == 'stone_work':
            await self.build.stone_work(user_data)
        elif action == 'ore_work':
            await self.build.ore_work(user_data)
        elif action == 'smith_work':
            await self.build.smith_work(user_data)
        elif action == 'wizard_work':
            await self.build.wizard_work(user_data)
        elif action == 'alchemist_work':
            await self.build.alchemist_work(user_data)
        elif action == 'warrior_work':
            await self.build.warrior_work(user_data)
        elif action == 'archer_work':
            await self.build.warrior_work(user_data)
        elif action == 'warlock_work':
            await self.build.warrior_work(user_data)

        elif action == 'wood_inwork':
            await self.citizen.inwork(user_data, 'wood', amount)
        elif action == 'stone_inwork':
            await self.citizen.inwork(user_data, 'stone', amount)
        elif action == 'ore_inwork':
            await self.citizen.inwork(user_data, 'ore', amount)
        elif action == 'smith_inwork':
            await self.citizen.inwork(user_data, 'smith', amount)
        elif action == 'wizard_inwork':
            await self.citizen.inwork(user_data, 'wizard', amount)
        elif action == 'alchemist_inwork':
            await self.citizen.inwork(user_data, 'alchemist', amount)
        elif action == 'warrior_inwork':
            await self.citizen.inwork(user_data, 'warrior', amount)
        elif action == 'archer_inwork':
            await self.citizen.inwork(user_data, 'archer', amount)
        elif action == 'warlock_inwork':
            await self.citizen.inwork(user_data, 'warlock', amount)

        await user_data.save()

        return await UserDataPydanic.from_tortoise_orm(user_data)

    async def find(self):
        return await self.war.random_enemies()

    async def attack(self, token, enemy_id):
        user = await UserData.filter(user__token=token).prefetch_related('user').get()
        await user.processing()
        enemy = await UserData.filter(user__id=enemy_id).prefetch_related('user').get()
        await enemy.processing()

        battle = await self.war.attack(user, enemy)
        await user.save()
        await enemy.save()
        return battle

    async def battles(self, token):
        user = await User.filter(token=token).get()
        return await Battle.filter(Q(Q(attack=user), Q(defender=user), join_type='OR')).prefetch_related('attack', 'defender').all().values('data', 'reward', 'time', 'win', 'attack__vk_id', 'attack__nickname', 'defender__vk_id', 'defender__nickname')


    async def level_up(self, token):
        return 'ok'

    async def extract(self, user_data, target):
        if user_data.energy < 1:
            return None

        if getattr(user_data, target) >= getattr(user_data, f'{target}_max')():
            return None

        user_data.energy -= 1
        user_data.exp += 1

        setattr(user_data, target, getattr(user_data, target) + 1)
