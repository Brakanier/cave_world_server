import random
import datetime

from tortoise.query_utils import Q
from fastapi import HTTPException

from models import User, UserPydanic, UserData, UserDataPydanic, Battle, BattlePydanic


class War:
    def __init__(self):
        pass
    
    async def random_enemies(self, user_id: int, level: int):
        count = await User.all().count()
        limit = 3
        #offset = random.randint(0, count - limit)
        #return await UserData.all().values('level', 'trophy','terrain', 'user__vk_id', 'user__id', 'user__nickname')
        time_now = int(datetime.datetime.utcnow().timestamp())
        return await UserData.exclude(user__id=user_id).filter(last_defend__lt=time_now - 3600, level__gte=level).order_by('last_defend').all().limit(limit).values('level', 'trophy','terrain', 'user__vk_id', 'user__id', 'user__nickname')

    async def attack(self, user: User, enemy: User):
        user_user, user = user, user.data
        enemy_user, enemy = enemy, enemy.data
        if user.warrior_inwork < 1:
            return

        user_army = user.warrior_inwork# + user.archer_inwork + user.warlock_inwork
        enemy_army = enemy.warrior_inwork# + enemy.archer_inwork + enemy.warlock_inwork

        delta = user_army - enemy_army
        reward = None
        if delta >= 0:
            win = True
            if enemy_army:
                reward = self.get_reward(enemy)
                user.terrain += reward['terrain']
                user.trophy += reward['trophy']
                user.wood = min(user.wood + reward['wood'], user.wood_max())
                user.stone = min(user.stone + reward['stone'], user.stone_max())
                user.iron += reward['iron']
                # user.orb += reward['orb']
                user.exp += reward['exp']
        else:
            win = False
        
        # user_warrior_die, user_archer_die, user_warlock_die = self.get_dead(user, enemy_army)
        # enemy_warrior_die, enemy_archer_die, enemy_warlock_die = self.get_dead(enemy, user_army)

        user_warrior_die = self.get_dead_war(user, enemy_army)
        enemy_warrior_die = self.get_dead_war(enemy, user_army)

        deads = None
        if user_warrior_die < user.warrior_inwork and enemy_warrior_die == enemy.warrior_inwork:
            deads = self.get_dead_citizens(user.warrior_inwork - user_warrior_die, enemy)
            print(deads)

        data = {
            'attack_warrior': user.warrior_inwork,
            # 'attack_archer': user.archer_inwork,
            # 'attack_warlock': user.warlock_inwork,
            'attack_warrior_die': user_warrior_die,
            # 'attack_archer_die': user_archer_die,
            # 'attack_warlock_die': user_warlock_die,
            'defender_warrior': enemy.warrior_inwork,
            # 'defender_archer': enemy.archer_inwork,
            # 'defender_warlock': enemy.warlock_inwork,
            'defender_warrior_die': enemy_warrior_die,
            # 'defender_archer_die': enemy_archer_die,
            # 'defender_warlock_die': enemy_warlock_die 
        }

        if deads:
            data["attack_warrior_die"] += deads["warriors"]
            del deads["warriors"]
            for key in deads:
                data[key] = deads[key]
        
        user.citizens -= user_warrior_die# + user_archer_die + user_warlock_die
        user.warrior_inwork -= user_warrior_die
        # user.archer_inwork -= user_archer_die
        # user.warlock_inwork -= user_warlock_die

        enemy.citizens -= enemy_warrior_die# + enemy_archer_die + enemy_warlock_die
        enemy.warrior_inwork -= enemy_warrior_die
        # enemy.archer_inwork -= enemy_archer_die
        # enemy.warlock_inwork -= enemy_warlock_die

        defend_time = int(datetime.datetime.utcnow().timestamp())
        enemy.last_defend = defend_time
        battle = await Battle.create(attack=user_user, defender=enemy_user, attack_vk_id=user_user.vk_id, defender_vk_id=enemy_user.vk_id, time=defend_time, win=win, data=data, reward=reward)
        return await BattlePydanic.from_tortoise_orm(battle)
        

    def get_dead_war(self, user: UserData, enemy_army: int):
        war = user.warrior_inwork - enemy_army
        if war < 0:
            war_die = user.warrior_inwork
        else:
            war_die = user.warrior_inwork - war
        return war_die

    def get_dead_citizens(self, warriors, enemy):
        deads = {
            'warriors': 0
        }
        if enemy.citizens == 0:
            return None

        if enemy.citizens_free() >= 1:
            free_dead = min(warriors*2, int(enemy.citizens_free()))
            deads["free"] = free_dead
            enemy.citizens -= free_dead
            warriors -= free_dead / 2
            deads['warriors'] += free_dead / 2
            if warriors <= 0:
                deads["warriors"] = round(deads["warriors"])
                return deads

        if enemy.smith_inwork > 0:
            smith_dead = min(warriors*2, enemy.smith_inwork)
            deads["smith"] = smith_dead
            enemy.citizens -= smith_dead
            enemy.smith_inwork -= smith_dead
            warriors -= smith_dead / 2
            deads['warriors'] += smith_dead / 2
            if warriors <= 0:
                deads["warriors"] = round(deads["warriors"])
                return deads

        if enemy.wood_inwork > 0:
            wood_dead = min(warriors*2, enemy.wood_inwork)
            deads["wood"] = wood_dead
            enemy.citizens -= wood_dead
            enemy.wood_inwork -= wood_dead
            warriors -= wood_dead / 2
            deads['warriors'] += wood_dead / 2
            if warriors <= 0:
                deads["warriors"] = round(deads["warriors"])
                return deads

        if enemy.stone_inwork > 0:
            stone_dead = min(warriors*2, enemy.stone_inwork)
            deads["stone"] = stone_dead
            enemy.citizens -= stone_dead
            enemy.stone_inwork -= stone_dead
            warriors -= stone_dead / 2
            deads['warriors'] += stone_dead / 2
            if warriors <= 0:
                deads["warriors"] = round(deads["warriors"])
                return deads
        
        deads["warriors"] = round(deads["warriors"])
        return deads
        
            

    def get_dead(self, user: UserData, enemy_army: int):
        war = user.warrior_inwork - enemy_army
        war_die = 0
        arch_die = 0
        warl_die = 0
        print('war', war)
        if war < 0:
            war_die = user.warrior_inwork
            if user.archer_inwork:
                arch = user.archer_inwork + war
                print('arch', arch)
                if arch < 0:
                    arch_die = user.archer_inwork
                    if user.warlock_inwork:
                        warl = user.warlock_inwork + arch
                        print('warl', warl)
                        if warl < 0:
                            warl_die = user.warlock_inwork
                        else:
                            warl_die = user.warlock_inwork + warl
                else:
                    arch_die = user.archer_inwork - arch
        else:
            war_die = user.warrior_inwork - war

        print('war_die', war_die)
        print('arch_die', arch_die)
        print('warl_die', warl_die)
        return war_die, arch_die, warl_die

    def get_reward(self, enemy: UserData):
        return {
            'trophy': random.randint(1, 10),
            'wood': random.randint(0, 30),
            'stone': random.randint(0, 30),
            'iron': random.randint(0, 10),
            # 'orb': random.randint(0, 10),
            'terrain': random.randint(1, 5),
            'exp': random.randint(1, 5)
        }