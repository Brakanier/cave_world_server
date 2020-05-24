from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

import datetime


class UserData(models.Model):
    """UserData model"""

    id = fields.IntField(pk=True)
    user = fields.OneToOneField("models.User", related_name="data")
    time = fields.BigIntField()
    last_defend = fields.BigIntField(default=0)

    exp = fields.BigIntField(default=0)
    level = fields.IntField(default=1)

    energy = fields.FloatField(default=30)
    terrain = fields.IntField(default=30)
    trophy = fields.IntField(default=0)

    # Ресурсы
    gold = fields.IntField(default=0)

    wood = fields.FloatField(default=100)
    stone = fields.FloatField(default=100)
    iron = fields.FloatField(default=100)

    # Население

    citizens = fields.FloatField(default=10)
    wood_inwork = fields.IntField(default=0)
    stone_inwork = fields.IntField(default=0)

    smith_inwork = fields.IntField(default=0)
    alchemist_inwork = fields.IntField(default=0)

    ## Армия
    warrior_inwork = fields.IntField(default=0)
    archer_inwork = fields.IntField(default=0)
    warlock_inwork = fields.IntField(default=0)

    # Здания
    ## Армия
    warrior_work = fields.IntField(default=0)
    archer_work = fields.IntField(default=0)
    warlock_work = fields.IntField(default=0)

    ## Добыча
    wood_work = fields.IntField(default=0)
    stone_work = fields.IntField(default=0)

    smith_work = fields.IntField(default=0)
    alchemist_work = fields.IntField(default=0)

    ## Склады
    wood_store = fields.IntField(default=0)
    stone_store = fields.IntField(default=0)

    ## Дома
    hut = fields.IntField(default=10)
    house = fields.IntField(default=0)
    mansion = fields.IntField(default=0)

    def current_exp(self) -> int:
        return self.exp - sum([self.need_exp(lvl) for lvl in range(self.level)])
    
    def need_exp(self, level: int = None) -> int:
        if level != None:
            return sum([lvl * 10 for lvl in range(level + 1)])
        else:
            return sum([lvl * 10 for lvl in range(self.level + 1)])

    def energy_max(self) -> int:
        return 30

    def wood_max(self) -> int:
        return 100 + 100 * self.wood_store

    def stone_max(self) -> int:
        return 100 + 100 * self.stone_store

    def citizens_max(self) -> int:
        return 1 * self.hut + 5 * self.house + 10 * self.mansion

    def citizens_free(self) -> int:
        return (
            self.citizens
            - self.wood_inwork
            - self.stone_inwork
            - self.smith_inwork
            - self.alchemist_inwork
            - self.warrior_inwork
            - self.archer_inwork
            - self.warlock_inwork
        )

    def terrain_free(self) -> int:
        return (
            self.terrain
            - self.hut
            - self.house
            - self.mansion
            - self.wood_store
            - self.stone_store
            - self.wood_work
            - self.stone_work
            - self.smith_work
            - self.alchemist_work
        )
    
    def warrior_max(self) -> int:
        return 5 * self.warrior_work
    
    def archer_max(self) -> int:
        return 3 * self.archer_work
    
    def warlock_max(self) -> int:
        return 1 * self.warlock_work

    async def processing(self):
        current = int(datetime.datetime.utcnow().timestamp())
        delta = current - self.time
        tics = delta / 60

        print(tics)

        # self.normalize('wood')
        # self.normalize('stone')
        # self.normalize('ore')
        # self.normalize('smith')
        # self.normalize('wizard')
        # self.normalize('alchemist')
        # if self.wood < 0 :
        #     self.wood = 0
        # if self.stone < 0:
        #     self.stone = 0
        # if self.ore < 0:
        #     self.ore = 0
        
        # 0.2 per minute
        if self.energy < 30:
            self.energy = min(self.energy + tics * 0.2, 30)

        if self.citizens < self.citizens_max():
            self.citizens = min(self.citizens + tics * 1, self.citizens_max())

        if self.wood_inwork and self.wood < self.wood_max():
            self.wood = min(self.wood + tics * 0.2 * self.wood_inwork, self.wood_max())

        if self.stone_inwork and self.stone < self.stone_max():
            self.stone = min(
                self.stone + tics * 0.2 * self.stone_inwork, self.stone_max()
            )
        
        # if self.ore_inwork:
        #     self.ore += tics * 0.2 * self.ore_inwork

        if self.smith_inwork:
            self.iron += tics * 0.1 * self.smith_inwork
        
        # if self.smith_inwork and self.ore >= 1:
        #     iron = min(tics * 0.1 * self.smith_inwork, self.ore)
        #     self.iron += iron
        #     self.ore -= iron
            
        
        # if self.wizard_inwork:
        #     self.orb += tics * 0.1 * self.wizard_inwork
        
        if self.alchemist_inwork:
            pass
            # self.alchemy += tics * 0.1 * self.alchemist_inwork

        # if self.warrior_inwork < 0:
        #     self.warrior_inwork = 0
        # if self.archer_inwork < 0:
        #     self.archer_inwork = 0
        # if self.warlock_inwork < 0:
        #     self.warlock_inwork


        self.time = current

    # def normalize(self, target: str):
    #     inwork = getattr(self, f'{target}_inwork')
    #     work = getattr(self, f'{target}_work')
    #     if inwork < 0:
    #         setattr(self, f'{target}_inwork', 0)
    #     elif inwork > work:
    #         setattr(self, f'{target}_inwork', work)


    class PydanticMeta:
        computed = [
            "current_exp",
            "need_exp",
            "terrain_free",
            "energy_max",
            "wood_max",
            "stone_max",
            "citizens_max",
            "citizens_free",
            "warrior_max",
            "archer_max",
            "warlock_max"
        ]
        exclude = ["id", "time"]


UserDataPydanic = pydantic_model_creator(UserData, name="UserData")
