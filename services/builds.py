
from models import UserData

class Builds:
    def __init__(self):
        pass
    
    # Дома
    async def hut(self, user_data: UserData):
        if user_data.wood >= 10:
            user_data.wood -= 10
            user_data.hut += 1
    
    async def house(self, user_data: UserData):
        if user_data.wood >= 15 and user_data.stone >= 15:
            user_data.wood -= 15
            user_data.stone -= 15
            user_data.house += 1
    
    async def mansion(self, user_data: UserData):
        if user_data.wood >= 30 and user_data.stone >= 30:
            user_data.wood -= 30
            user_data.stone -= 30
            user_data.mansion += 1
    
    # Склады
    async def wood_store(self, user_data: UserData):
        if user_data.wood >= 30 and user_data.stone >= 30:
            user_data.wood -= 30
            user_data.stone -= 30
            user_data.wood_store += 1
    
    async def stone_store(self, user_data: UserData):
        if user_data.wood >= 30 and user_data.stone >= 30:
            user_data.wood -= 30
            user_data.stone -= 30
            user_data.stone_store += 1

    # Добыча
    async def wood_work(self, user_data: UserData):
        if user_data.wood >= 10 and user_data.stone >= 10:
            user_data.wood -= 10
            user_data.stone -= 10
            user_data.wood_work += 1
    
    async def stone_work(self, user_data: UserData):
        if user_data.wood >= 10 and user_data.stone >= 10:
            user_data.wood -= 10
            user_data.stone -= 10
            user_data.stone_work += 1
    
    async def ore_work(self, user_data: UserData):
        if user_data.wood >= 10 and user_data.stone >= 10:
            user_data.wood -= 10
            user_data.stone -= 10
            user_data.ore_work += 1
    
    # Спец
    async def smith_work(self, user_data: UserData):
        if user_data.wood >= 10 and user_data.stone >= 10:
            user_data.wood -= 10
            user_data.stone -= 10
            user_data.smith_work += 1

    async def wizard_work(self, user_data: UserData):
        if user_data.wood >= 10 and user_data.stone >= 10:
            user_data.wood -= 10
            user_data.stone -= 10
            user_data.wizard_work += 1

    async def alchemist_work(self, user_data: UserData):
        if user_data.wood >= 10 and user_data.stone >= 10:
            user_data.wood -= 10
            user_data.stone -= 10
            user_data.alchemist_work += 1    

    # Армия
    async def warrior_work(self, user_data: UserData):
        if user_data.wood >= 10 and user_data.stone >= 10:
            user_data.wood -= 10
            user_data.stone -= 10
            user_data.warrior_work += 1
    
    async def archer_work(self, user_data: UserData):
        if user_data.wood >= 10 and user_data.stone >= 10:
            user_data.wood -= 10
            user_data.stone -= 10
            user_data.archer_work += 1
    
    async def warlock_work(self, user_data: UserData):
        if user_data.wood >= 10 and user_data.stone >= 10:
            user_data.wood -= 10
            user_data.stone -= 10
            user_data.warlock_work += 1