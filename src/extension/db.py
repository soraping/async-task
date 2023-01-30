from peewee_async import PooledMySQLDatabase, MySQLDatabase
from playhouse.shortcuts import ReconnectMixin


class BaseMysqlDB:
    _instance = None


class MySQLDatabaseConnection(MySQLDatabase, BaseMysqlDB):
    @classmethod
    def get_db_instance(cls, db_config):
        if not cls._instance:
            cls._instance = cls(**db_config)
        return cls._instance


class ReconnectMySQLDatabase(ReconnectMixin, MySQLDatabaseConnection):
    """
    可断线重连db
    """
    pass


class ReconnectAsyncPooledMySQLDatabase(ReconnectMixin, PooledMySQLDatabase, BaseMysqlDB):
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
