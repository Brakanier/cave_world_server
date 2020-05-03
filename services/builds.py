
from models import UserData

class Builds:
    def __init__(self):
        pass

    async def wood_store(self, user_data: UserData):
        if user_data.wood >= 30 and user_data.stone >= 30:
            user_data.wood -= 30
            user_data.stone -= 30
            user_data.wood_store += 1
        
    async def hut(self, user_data: UserData):
        if user_data.wood >= 10:
            user_data.wood -= 10
            user_data.hut += 1

    async def wood_work(self, user_data: UserData):
        if user_data.wood >= 10 and user_data.stone >= 10:
            user_data.wood -= 10
            user_data.stone -= 10
            user_data.wood_work += 1