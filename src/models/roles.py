import datetime

from peewee import (
    Model,
    CharField,
    DateTimeField,
    PrimaryKeyField
)


class Role(Model):
    id = PrimaryKeyField()
    name = CharField(max_length=20, verbose_name='role name')
    create_time = DateTimeField(verbose_name='role create time', default=datetime.datetime.utcnow)

    class Meta:
        table_name = 'roles'