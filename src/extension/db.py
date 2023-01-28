from peewee import Proxy
from peewee_async import PooledMySQLDatabase, MySQLDatabase
from playhouse.shortcuts import ReconnectMixin

# 连接库代理
db = Proxy()


class ReconnectBaseMysqlDB:
    _instance = None


class ReconnectMySQLDatabase(ReconnectMixin, MySQLDatabase, ReconnectBaseMysqlDB):
    """
    可断线重连db
    """

    @classmethod
    def get_db_instance(cls, db_config):
        if not cls._instance:
            cls._instance = cls(**db_config)
        return cls._instance


class ReconnectAsyncPooledMySQLDatabase(ReconnectMixin, PooledMySQLDatabase, ReconnectBaseMysqlDB):
    """
    可断线重连的异步db连接池
    """

    @classmethod
    def get_db_instance(cls, db_config):
        if not cls._instance:
            cls._instance = cls(**db_config, max_connections=10)
        return cls._instance
