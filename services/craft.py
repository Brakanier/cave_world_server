from models import User, Item

class Craft:
    def __init__(self):
        pass
    
    async def craft(self, user: User, item: str):
        if item == 'wood_pickaxe':
            return await self.craft_wood_pickaxe(user)
        
        return False

    async def craft_wood_pickaxe(self, user: User):
        exist = next(filter(lambda i: i.id_name == 'wood_pickaxe', await user.items), None)
        if exist:
            print('exists')
            return False
        
        if user.data.wood < 30:
            print('need wood')
            return False
        
        item = await Item.create(user=user, name="Деревянная кирка", id_name="wood_pickaxe")
        user.items.append(item)
        
        return True