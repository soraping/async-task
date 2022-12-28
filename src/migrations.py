from datetime import datetime
from playhouse.migrate import MySQLDatabase, MySQLMigrator, Model
from peewee import (
    PrimaryKeyField,
    CharField,
    DateTimeField
)
from config import CONFIG

config_dict = CONFIG.get_config()
db_manager = MySQLDatabase(**config_dict['mysql'])
migrator = MySQLMigrator(db_manager)


class MigrationRecord(Model):
    """
    表操作模型
    """
    id = PrimaryKeyField()
    table = CharField()
    version = CharField()
    author = CharField()
    create_time = DateTimeField(verbose_name='创建时间',
                                default=datetime.utcnow(), help_text='表操作记录')

    class Meta:
        table_name = 'migration_record'
        database = db_manager


class MigrationModel:
    _db = db_manager
    _migrator = migrator

    def __init__(self, model):
        # 操作记录初始化
        self._mr = MigrationRecord()
        self._db.create_tables(([self._mr]), safe=True)

        # 对应模型
        self._model = model
        self._model._meta.database = self._db
        self._model.create_table(safe=True)
        self._name = self._model._meta.table_name

    def add_column(self, col, field=None):
        """
        新增字段
        :param col:
        :param field:
        :return:
        """
        print('Migrating==> [%s] add_column: %s' % (self._name, col))
        field = getattr(self._model, col) if not field else field
        return self._migrator.add_column(self._name, col, field)



if __name__ == '__main__':
    ...
