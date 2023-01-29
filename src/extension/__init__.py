from peewee_async import Manager
from .aio_mongo import MotorBase
from .aio_redis import RedisSession
from .db import ReconnectMySQLDatabase, ReconnectAsyncPooledMySQLDatabase
from .jwt import JwtExt
from src.models import database_proxy


def init_mysql(db_config) -> Manager:
    """
    初始化mysql, 返回 Manager 实例
    :param db_config:
    :return:
    """
    mysql_db = ReconnectMySQLDatabase.get_db_instance(db_config)
    database_proxy.initialize(mysql_db)
    mgr = Manager(mysql_db)
    return mgr


__all__ = [
    JwtExt,
    MotorBase,
    RedisSession,
    init_mysql
]
