from peewee import (
    CharField,
    PrimaryKeyField
)
from src.models.base import BaseModel


class GoodsModel(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=20, verbose_name='goods name')

    class Meta:
        table_name = 'goods'
