
from models import UserData

class Builds:
    def __init__(self):
        pass
    
    # Дома
    async def hut(self, user_data: UserData):
        wood = 10 + 10 * user_data.hut
        if user_data.wood >= wood:
            user_data.wood -= wood
            user_data.hut += 1
            user_data.citizens += 1
    
    async def house(self, user_data: UserData):
        wood = 15 + 15 * user_data.house
        stone = 15 + 15 * user_data.house
        if user_data.wood >= wood and user_data.stone >= stone:
            user_data.wood -= wood
            user_data.stone -= stone
            user_data.house += 1
            user_data.citizens += 5
    
    async def mansion(self, user_data: UserData):
        wood = 30 + 30 * user_data.mansion
        stone = 30 + 30 * user_data.mansion
        if user_data.wood >= wood and user_data.stone >= stone:
            user_data.wood -= wood
            user_data.stone -= stone
            user_data.mansion += 1
            user_data.citizens += 10
    
    # Склады
    async def wood_store(self, user_data: UserData):
        wood = 30 + 30 * user_data.wood_store
        stone = 30 + 30 * user_data.wood_store
        if user_data.wood >= wood and user_data.stone >= stone:
            user_data.wood -= wood
            user_data.stone -= stone
            user_data.wood_store += 1
    
    async def stone_store(self, user_data: UserData):
        wood = 30 + 30 * user_data.stone_store
        stone = 30 + 30 * user_data.stone_store
        if user_data.wood >= wood and user_data.stone >= wood:
            user_data.wood -= wood
            user_data.stone -= stone
            user_data.stone_store += 1

    # Добыча
    async def wood_work(self, user_data: UserData):
        wood = 10 + 10 * user_data.wood_work
        stone = 10 + 10 * user_data.wood_work
        if user_data.wood >= wood and user_data.stone >= stone:
            user_data.wood -= wood
            user_data.stone -= stone
            user_data.wood_work += 1
    
    async def stone_work(self, user_data: UserData):
        wood = 10 + 10 * user_data.stone_work
        stone = 10 + 10 * user_data.stone_work
        if user_data.wood >= wood and user_data.stone >= stone:
            user_data.wood -= wood
            user_data.stone -= stone
            user_data.stone_work += 1
    
    async def ore_work(self, user_data: UserData):
        wood = 10 + 10 * user_data.ore_work
        stone = 10 + 10 * user_data.ore_work
        if user_data.wood >= wood and user_data.stone >= stone:
            user_data.wood -= wood
            user_data.stone -= stone
            user_data.ore_work += 1
    
    # Спец
    async def smith_work(self, user_data: UserData):
        wood = 10 + 10 * user_data.smith_work
        stone = 10 + 10 * user_data.smith_work
        ore = 10 + 10 * user_data.smith_work
        if user_data.wood >= wood and user_data.stone >= stone and user_data.ore >= ore:
            user_data.wood -= wood
            user_data.stone -= stone
            user_data.ore -= ore
            user_data.smith_work += 1

    async def wizard_work(self, user_data: UserData):
        wood = 10 + 10 * user_data.wizard_work
        stone = 10 + 10 * user_data.wizard_work
        ore = 10 + 10 * user_data.wizard_work
        iron = 10 + 10 * user_data.wizard_work
        if user_data.wood >= wood and user_data.stone >= stone and user_data.ore >= ore and user_data.iron >= iron:
            user_data.wood -= wood
            user_data.stone -= stone
            user_data.ore -= ore
            user_data.iron -= iron
            user_data.wizard_work += 1

    async def alchemist_work(self, user_data: UserData):
        wood = 10 + 10 * user_data.alchemist_work
        stone = 10 + 10 * user_data.alchemist_work
        ore = 10 + 10 * user_data.alchemist_work
        iron = 10 + 10 * user_data.alchemist_work
        orb = 10 + 10 * user_data.alchemist_work
        if user_data.wood >= wood and user_data.stone >= stone and user_data.ore >= ore and user_data.iron >= iron and user_data.orb >= orb:
            user_data.wood -= wood
            user_data.stone -= stone
            user_data.iron -= iron
            user_data.orb -= orb
            user_data.alchemist_work += 1    

    # Армия
    async def warrior_work(self, user_data: UserData):
        wood = 10 + 10 * user_data.warrior_work
        stone = 10 + 10 * user_data.warrior_work
        iron = 10 + 10 * user_data.warrior_work
        if user_data.wood >= wood and user_data.stone >= stone and user_data.iron >= iron:
            user_data.wood -= wood
            user_data.stone -= stone
            user_data.iron -= iron
            user_data.warrior_work += 1
    
    async def archer_work(self, user_data: UserData):
        wood = 20 + 20 * user_data.archer_work
        stone = 20 + 20 * user_data.archer_work
        iron = 10 + 10 * user_data.archer_work
        if user_data.wood >= wood and user_data.stone >= stone and user_data.iron >= iron:
            user_data.wood -= wood
            user_data.stone -= stone
            user_data.iron -= iron
            user_data.archer_work += 1
    
    async def warlock_work(self, user_data: UserData):
        wood = 30 + 30 * user_data.warlock_work
        stone = 30 + 30 * user_data.warlock_work
        iron = 10 + 10 * user_data.warlock_work
        orb = 10 + 10 * user_data.warlock_work
        if user_data.wood >= wood and user_data.stone >= stone and user_data.iron >= iron and user_data.orb >= orb:
            user_data.wood -= wood
            user_data.stone -= stone
            user_data.iron -= iron
            user_data.orb -= orb
            user_data.warlock_work += 1