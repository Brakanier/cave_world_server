from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from .user_data import UserData
from .item import Item

class User(models.Model):
    """User model"""
    id = fields.IntField(pk=True)
    vk_id = fields.IntField(unique=True, index=True)
    token = fields.CharField(512, unique=True)
    created = fields.DatetimeField(auto_now_add=True)
    data = fields.ReverseRelation["UserData"]
    nickname = fields.CharField(18, null=True)
    data: fields.ReverseRelation[UserData]
    items: fields.ReverseRelation[Item]
    
UserPydanic = pydantic_model_creator(User, name="User", exclude=['token'])
NewUserPydanic = pydantic_model_creator(User, name="NewUser", exclude=['id', 'created'])