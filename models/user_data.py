from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

import datetime

class UserData(models.Model):
    """UserData model"""
    id = fields.IntField(pk=True)
    user = fields.OneToOneField('models.User', related_name='data')
    time = fields.BigIntField()
    energy = fields.FloatField(default=30)
    wood = fields.FloatField(default=0)
    stone = fields.FloatField(default=0)
    

    async def processing(self):
        current = int(datetime.datetime.utcnow().timestamp())
        delta = current - self.time
        tics = delta / 60
        # 0.2 per minute
        self.energy += tics * 0.2
        print(tics * 0.2)
        self.time += tics * 60


UserDataPydanic = pydantic_model_creator(UserData, name="UserData", exclude=['id', 'time'])