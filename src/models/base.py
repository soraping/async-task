import datetime
from peewee import (
    DateTimeField,
    Model
)

from src.extension import db


class BaseModel(Model):
    create_time = DateTimeField(default=datetime.datetime.utcnow, formats='%Y-%m-%d %H:%M:%S',
                                verbose_name='create time')
    update_time = DateTimeField(default=datetime.datetime.utcnow, formats='%Y-%m-%d %H:%M:%S',
                                verbose_name='modify time')

    class Meta:
        database = db
