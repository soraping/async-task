from peewee import MySQLDatabase
from peewee_async import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin


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



if __name__ == '__main__':
    print(isinstance(ReconnectMySQLDatabase({}), MySQLDatabase))