
from models import UserData

class Citizens:
    def __init__(self):
        pass
    
    async def wood_inwork(self, user_data: UserData, amount: int):
        if amount > 0 and user_data.citizens_free() >= amount and user_data.wood_inwork + amount <= user_data.wood_work:
            user_data.wood_inwork += amount
        elif user_data.wood_inwork + amount >= 0:
            user_data.wood_inwork += amount
