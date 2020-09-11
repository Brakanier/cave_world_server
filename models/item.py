from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Item(models.Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation["User"] = fields.OneToOneField("models.User", related_name="items")
    name = fields.CharField(32)
    id_name = fields.CharField(32)