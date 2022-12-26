import datetime
from peewee import (
    DateTimeField,
    Model,
    Proxy
)

db = Proxy()


class BaseModel(Model):
    create_time = DateTimeField(default=datetime.datetime.utcnow, formats='%Y-%m-%d %H:%M:%S',
                                verbose_name='create time')
    update_time = DateTimeField(default=datetime.datetime.utcnow, formats='%Y-%m-%d %H:%M:%S',
                                verbose_name='modify time')

    class Meta:
        db = db
