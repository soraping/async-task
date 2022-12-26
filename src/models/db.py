from peewee_async import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin


class ReconnectAsyncPooledMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    """
    可断线重连的db实例
    """
    _instance = None

    @classmethod
    def get_db_instance(cls, db_config):
        if not cls._instance:
            cls._instance = cls(**db_config, max_connections=10)
        return cls._instance
