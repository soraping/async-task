from peewee_async import Manager, MySQLDatabase
from .aio_mongo import MotorBase
from .aio_redis import RedisSession
from .db import ReconnectMySQLDatabase
from .jwt import JwtExt


class InitMysql:
    _db = None

    def __init__(self, db_config):
        self.config = db_config

    def db(self) -> MySQLDatabase:
        """
        初始化mysql, 返回 MySQLDatabase 实例
        :return:
        """
        if InitMysql._db is None:
            InitMysql._db = ReconnectMySQLDatabase.get_db_instance(self.config)
        return InitMysql._db

    def __call__(self):
        return self.db()

    def mgr(self) -> Manager:
        """
        初始化mysql, 返回 Manager 实例
        :return:
        """
        return Manager(self.db())


__all__ = [
    'JwtExt',
    'MotorBase',
    'RedisSession',
    'InitMysql'
]
