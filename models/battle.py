from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Battle(models.Model):
    """Battle model"""
    id = fields.IntField(pk=True)
    attack = fields.ForeignKeyField("models.User", related_name="attacks")
    defender = fields.ForeignKeyField("models.User", related_name="defends")
    win = fields.BooleanField()
    time = fields.BigIntField()
    data = fields.JSONField()
    reward = fields.JSONField(null=True)
        
    
BattlePydanic = pydantic_model_creator(Battle, name="Battle", exclude=['id'])