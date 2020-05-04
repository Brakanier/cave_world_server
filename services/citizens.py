
from models import UserData

class Citizens:
    def __init__(self):
        pass
    
    async def wood_inwork(self, user_data: UserData, amount: int):
        if amount > 0 and user_data.citizens_free() >= amount and user_data.wood_inwork + amount <= user_data.wood_work:
            user_data.wood_inwork += amount
        elif user_data.wood_inwork + amount >= 0:
            user_data.wood_inwork += amount
    
    async def stone_inwork(self, user_data: UserData, amount: int):
        if amount > 0 and user_data.citizens_free() >= amount and user_data.stone_inwork + amount <= user_data.stone_work:
            user_data.stone_inwork += amount
        elif user_data.stone_inwork + amount >= 0:
            user_data.stone_inwork += amount

    async def inwork(self, user_data: UserData, target: str, amount: int):
        inwork = getattr(user_data, f'{target}_inwork')
        after_inwork = inwork + amount

        if amount > 0 and user_data.citizens_free() and after_inwork <= inwork:
            setattr(user_data, f'{target}_inwork', after_inwork)
        else:
            setattr(user_data, f'{target}_inwork', after_inwork)

        