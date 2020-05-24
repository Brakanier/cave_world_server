import datetime

from tortoise.expressions import F
from tortoise.transactions import atomic
from tortoise.query_utils import Q, Prefetch
from fastapi import HTTPException

from models import User, UserData, UserDataPydanic, Battle
from .builds import Builds
from .citizens import Citizens
from .war import War

class Game:
    def __init__(self, find, notify):
        self.notify = notify
        self.find = find
        self.build = Builds()
        self.citizen = Citizens()
        self.war = War()
    
    async def action(self, user_id: int, data: dict):
        user_connect = self.find(user_id)
        if not user_connect:
            return
        user = user_connect.user
        await user.data.processing()

        if data["action"] == 'wood':
            await self.extract(user.data, 'wood')
        elif data["action"] == 'stone':
            await self.extract(user.data, 'stone')
        
        elif data["action"] == 'hut':
            await self.build.hut(user.data)
        elif data["action"] == 'house':
            await self.build.house(user.data)
        elif data["action"] == 'mansion':
            await self.build.mansion(user.data)

        elif data["action"] == 'wood_store':
            await self.build.wood_store(user.data)
        elif data["action"] == 'stone_store':
            await self.build.stone_store(user.data)
        
        elif data["action"] == 'wood_work':
            await self.build.wood_work(user.data)
        elif data["action"] == 'stone_work':
            await self.build.stone_work(user.data)
        elif data["action"] == 'smith_work':
            await self.build.smith_work(user.data)
        elif data["action"] == 'alchemist_work':
            await self.build.alchemist_work(user.data)
        elif data["action"] == 'warrior_work':
            await self.build.warrior_work(user.data)
        # elif data["action"] == 'archer_work':
        #     await self.build.archer_work(user.data)
        # elif data["action"] == 'warlock_work':
        #     await self.build.warlock_work(user.data)

        elif data["action"] == 'wood_inwork':
            await self.citizen.inwork(user.data, 'wood', data['amount'])
        elif data["action"] == 'stone_inwork':
            await self.citizen.inwork(user.data, 'stone', data['amount'])
        elif data["action"] == 'smith_inwork':
            await self.citizen.inwork(user.data, 'smith', data['amount'])
        elif data["action"] == 'alchemist_inwork':
            await self.citizen.inwork(user.data, 'alchemist', data['amount'])
        elif data["action"] == 'warrior_inwork':
            await self.citizen.inwork(user.data, 'warrior', data['amount'])
        # elif data["action"] == 'archer_inwork':
        #     await self.citizen.inwork(user.data, 'archer', data['amount'])
        # elif data["action"] == 'warlock_inwork':
        #     await self.citizen.inwork(user.data, 'warlock', data['amount'])

        elif data["action"] == 'find':
            enemies = await self.war.random_enemies(user_id=user.id)
            await self.send(user.id, 'enemies', enemies)
        elif data["action"] == 'attack':
            # get user and enemy
            enemy_connect = self.find(data["id"])
            if enemy_connect:
                enemy_user = enemy_connect.user
            else:
                enemy = await UserData.filter(user__id=data["id"]).prefetch_related('user').get_or_none()
                enemy_user = enemy.user if enemy else None
            if not enemy_user:
                return
            
            await self.attack(user, enemy_user)

        elif data['action'] == 'battles':
            battles = await self.battles(user)
            await self.send(user.id, 'battles', battles)

        if user.data.current_exp() >= user.data.need_exp():
            reward = await self.level_up(user.data)
            data = {
                'reward': reward,
                'current_exp': user.data.current_exp(),
                'need_exp': user.data.need_exp(),
                'exp': user.data.exp,
            }
            await self.send(user.id, 'levelup', data)

        await user.data.save()
        await UserDataPydanic.from_tortoise_orm(user.data)

    @atomic()
    async def attack(self, user: User, enemy: User):
        await enemy.data.processing()

        battle = await self.war.attack(user, enemy)
        if battle:
            await self.send(enemy.id, 'onattack', battle.dict())
            await self.send(user.id, 'attack', battle.dict())
            await enemy.data.save()

    async def battles(self, user: User):
        return await Battle.filter(Q(Q(attack=user), Q(defender=user), join_type='OR')).prefetch_related('attack', 'defender').order_by('-time').all().limit(10).values('data', 'reward', 'time', 'win', 'attack__vk_id', 'attack__nickname', 'defender__vk_id', 'defender__nickname')


    async def level_up(self, user_data: UserData):
        energy = 30
        terrain = 5 * user_data.level
        gold = 10 * user_data.level
        reward = {
            'energy': energy,
            'terrain': terrain,
            'gold': gold
        }
        user_data.energy += energy
        user_data.terrain += terrain
        user_data.gold += gold
        user_data.level += 1
        return reward

    async def extract(self, user_data, target):
        if user_data.energy < 1:
            return

        if getattr(user_data, target) >= getattr(user_data, f'{target}_max')():
            return

        user_data.energy -= 1
        user_data.exp += 1

        setattr(user_data, target, getattr(user_data, target) + 1)

    async def send(self, user_id: int, type: str, data: dict):
        await self.notify(user_id, {'type': type, 'data': data})