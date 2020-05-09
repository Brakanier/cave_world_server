from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

import datetime


class UserData(models.Model):
    """UserData model"""

    id = fields.IntField(pk=True)
    user = fields.OneToOneField("models.User", related_name="data")
    time = fields.BigIntField()

    exp = fields.BigIntField(default=0)
    level = fields.IntField(default=1)

    energy = fields.FloatField(default=30)
    terrain = fields.IntField(default=100)
    trophy = fields.IntField(default=0)

    # Ресурсы
    gold = fields.IntField(default=0)

    wood = fields.FloatField(default=0)
    stone = fields.FloatField(default=0)

    ore = fields.FloatField(default=0)
    iron = fields.FloatField(default=0)
    orb = fields.FloatField(default=0)
    alchemy = fields.FloatField(default=0)

    # Население

    citizens = fields.FloatField(default=0)
    wood_inwork = fields.IntField(default=0)
    stone_inwork = fields.IntField(default=0)
    ore_inwork = fields.IntField(default=0)

    smith_inwork = fields.IntField(default=0)
    wizard_inwork = fields.IntField(default=0)
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
    ore_work = fields.IntField(default=0)

    smith_work = fields.IntField(default=0)
    wizard_work = fields.IntField(default=0)
    alchemist_work = fields.IntField(default=0)

    ## Склады
    wood_store = fields.IntField(default=0)
    stone_store = fields.IntField(default=0)
    ore_store = fields.IntField(default=0)

    ## Дома
    hut = fields.IntField(default=0)
    house = fields.IntField(default=0)
    mansion = fields.IntField(default=0)

    def current_exp(self) -> int:
        return self.exp - sum([lvl * 10 for lvl in range(self.level)])
    
    def need_exp(self) -> int:
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
            - self.ore_inwork
            - self.smith_inwork
            - self.wizard_inwork
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
            - self.ore_store
            - self.wood_work
            - self.stone_work
            - self.ore_work
            - self.smith_work
            - self.wizard_work
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
        
        if self.ore_inwork:
            self.ore += tics * 0.2 * self.ore_inwork

        if self.smith_inwork and self.ore >= 1:
            iron = min(tics * 0.1 * self.smith_inwork, self.ore)
            self.iron += iron
            self.ore -= iron
        
        if self.wizard_inwork:
            self.orb += tics * 0.1 * self.wizard_inwork
        
        if self.alchemist_inwork:
            self.alchemy += tics * 0.1 * self.alchemist_inwork

        self.time = current


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
