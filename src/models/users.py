import datetime
from roles import Role

from peewee import (
    Model,
    DateTimeField,
    IntegerField,
    PrimaryKeyField,
    CharField,
    ForeignKeyField
)


class UserModel(Model):
    id = PrimaryKeyField()
    username = CharField(max_length=20, verbose_name='user name')
    age = IntegerField(null=False, verbose_name='user age')
    role_id = ForeignKeyField(model=Role, on_delete='SET NULL', verbose_name='role for user')
    create_time = DateTimeField(verbose_name='user create time', default=datetime.datetime.utcnow)

    class Meta:
        table_name = 'user'
