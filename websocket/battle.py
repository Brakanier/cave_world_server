
import uuid
from typing import List
import random

from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket, WebSocketState

import models
# from .connections import UserConnect, connections
# import services

# game = services.Game(connections.find, connections.notify)



class User:
    def __init__(self, websocket: WebSocket):
        self.ws = websocket
        self.id = str(uuid.uuid4())
        self.war = random.randint(1, 10)
        self.arch = random.randint(1, 10)
        self.wiz = random.randint(1, 10)
        self.hp = 0
        self.damage = 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'hp': self.hp,
            'damage': self.damage,
            'war': self.war,
            'arch': self.arch,
            'wiz': self.wiz
            }

    async def notify(self, data: dict):
        await self.ws.send_json(data)

class Battle:
    def __init__(self, users: List[User]):
        self.users: List[User] = users
        self.steps = {}
        self.round = 1
    
    def reset_users(self):
        for user in self.users:
            user.damage = 0
    
    async def sendAll(self, data):
        for user in self.users:
            await user.notify(data)
    
    async def process(self, user):
        enemy = next(filter(lambda u: u.id != user.id, self.users), None)
        user_step = self.steps[user.id]
        enemy_step = self.steps[enemy.id]

        

        user_step_a = getattr(user, user_step[0])
        user_step_d = getattr(enemy, user_step[1])
        enemy_step_a = getattr(enemy, enemy_step[0])
        enemy_step_d = getattr(user, enemy_step[1])

        
        print('USER STEP', user_step)
        print('ENEMY STEP', enemy_step)
        if user_step[0] == enemy_step[1] and user_step[1] == enemy_step[0]:
            print('ALL COLLISION')
            user.damage += max(user_step_a - user_step_d, 0)
            enemy.damage += max(enemy_step_a - enemy_step_d, 0)
            setattr(user, user_step[0], max(user_step_a - user_step_d, 0))
            setattr(enemy, enemy_step[0], max(enemy_step_a - enemy_step_d, 0))
        elif user_step[0] == enemy_step[1]:
            print('ONE COLLISION USER A - ENEMY D')
            user_part = user_step_a / 2

            # step
            user_step1_alive = max(user_part - user_step_d, 0)
            setattr(enemy, user_step[1], max(user_step_d - user_part, 0))
            
            # step
            user_step2_alive = max(user_part - enemy_step_a, 0)
            setattr(enemy, enemy_step[0], max(enemy_step_a - user_part, 0))
            # collision
            setattr(user, user_step[0], max(user_step1_alive + user_step2_alive, 0))
            user.damage += max(user_part - user_step_d, 0)
            enemy.damage += max(enemy_step_a - user_part, 0)
        elif user_step[1] == enemy_step[0]:
            print('ONE COLLISION USER D - ENEMY A')
            enemy_part = user_step_d / 2

            # step
            enemy_step1_alive = max(enemy_part - user_step_a, 0)
            setattr(user, user_step[0], max(user_step_a - enemy_part, 0))

            # step
            enemy_step2_alive = max(enemy_part - enemy_step_d, 0)
            setattr(user, enemy_step[1], max(enemy_step_d - enemy_part, 0))
            # collision
            setattr(enemy, user_step[1], max(enemy_step1_alive + enemy_step2_alive, 0))
            user.damage += max(user_step_a - enemy_part, 0)
            enemy.damage += max(enemy_part - enemy_step_d, 0)
        else:
            print('NO COLLISION')
            # step
            setattr(user, user_step[0], max(user_step_a - user_step_d, 0))
            setattr(enemy, user_step[1], max(user_step_d - user_step_a, 0))
            # step
            setattr(enemy, enemy_step[0], max(enemy_step_a - enemy_step_d, 0))
            setattr(user, enemy_step[1], max(enemy_step_d - enemy_step_a, 0))
            print('USER DAMAGE', user_step_a - user_step_d)
            print('ENEMY DAMAGE', enemy_step_a - enemy_step_d)
            user.damage += max(user_step_a - user_step_d, 0)
            enemy.damage += max(enemy_step_a - enemy_step_d, 0)
        result = {
            'type': 'round',
            'steps': self.steps
        }
        result[user.id] = user.to_dict()
        result[enemy.id] = enemy.to_dict()
        await self.sendAll(result)
        self.steps.clear()
        self.round += 1


    async def destroy(self):
        print('BATTLE DESTROY START', self.users)
        for user in self.users:
            print('REMOVE USER', user)
            if user.ws.client_state != WebSocketState.DISCONNECTED:
                find_list.append(user)
        self.users = []
        print('BATTLE DESTROY END', self.users)

    async def finish(self):
        user_copy = self.users.copy()
        self.users = []
        for user in user_copy:
            if user.ws.client_state != WebSocketState.DISCONNECTED:
                await user.ws.close()

find_list: List[User] = []
battles_list: List[Battle] = []

class BattleEndPoint(WebSocketEndpoint):
    encoding = "json"

    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()
        user = User(websocket)
        await user.notify({'type': 'connect', 'user': user.to_dict()})
        if len(find_list) == 0:
            print('ADD TO FIND')
            find_list.append(user)
        else:
            print('CREATE BATTLE')
            enemy = find_list.pop()
            
            # create battle
            battle = Battle([user, enemy])
            battles_list.append(battle)

            # notify start battle
            await user.notify({'type': 'start', 'enemy': enemy.to_dict()})
            await enemy.notify({'type': 'start', 'enemy': user.to_dict()})
        
        print(len(battles_list))
        print(len(find_list))
    
    async def on_receive(self, websocket: WebSocket, data: dict):

        if data["type"] == 'step':
            battle = next(filter(lambda battle: filter(lambda user: user.ws == websocket, battle.users), battles_list), None)
            if battle:
                user = next(filter(lambda user: user.ws == websocket, battle.users), None)
                if len(battle.steps) == 1 and user.id not in battle.steps:
                    print('battle processing')
                    print('ROUND', battle.round)
                    print(battle.steps)
                    battle.steps[user.id] = (data["from"], data["to"])
                    await battle.process(user)
                    
                    if battle.round == 3:
                        print('FINISH BATTLE')
                        await battle.finish()
                elif len(battle.steps) == 0:
                    print('save step')
                    battle.steps[user.id] = (data["from"], data["to"])
                else:
                    print('ignore')
            

    async def on_disconnect(self, websocket: WebSocket, close_code):
        print('START DISCONNECT', find_list)
        battle = next(filter(lambda battle: filter(lambda user: user.ws == websocket, battle.users), battles_list), None)
        if battle:
            print('BATTLE', battle, len(battle.users))
            await battle.destroy()
            battles_list.remove(battle)
            print('BATTLE', battle, len(battle.users))
        user = next(filter(lambda user: user.ws == websocket, find_list), None)
        print('USER', user)
        if user:
            find_list.remove(user)
        print('END DISCONNECT', find_list)
    
