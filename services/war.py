import random
from models import User, UserPydanic, UserData, UserDataPydanic

class War:
    def __init__(self):
        pass
    
    async def random_enemies(self):
        count = await User.all().count()
        #limit = 3
        #offset = random.randint(0, count - limit)
        #return await UserPydanic.from_queryset(User.all().limit(limit).offset(offset).prefetch_related(UserData.get('terrain')))
        return await UserData.all().values('terrain', 'user__vk_id', 'user__id')

    async def attack(self, user: UserData, enemy: UserData):
        return True
        