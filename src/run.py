from sanic import Sanic
from peewee_async import Manager
from sanic_openapi import openapi3_blueprint
from sanic_redis_ext import RedisExtension

from src.config import CONFIG
from werkzeug.utils import find_modules, import_string
from models import RedisSession, ReconnectMySQLDatabase, db as db_proxy

app = Sanic(name='async-task')
app.config.update(CONFIG.get_config())
#
# # 注册 redis
# RedisExtension(app)

# 注册 swagger
app.blueprint(openapi3_blueprint)


def register_blueprints(api_module: str, app: Sanic) -> None:
    """
    自动加载bp
    :param api_module:
    :param app:
    :return:
    """
    for name in find_modules(api_module, recursive=True):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.blueprint(mod.bp)


register_blueprints('views', app)


@app.after_server_start
async def setup(app: Sanic, loop) -> None:
    print("app start")
    print("swagger: {}/swagger".format(app.serve_location))

    # 注册 mysql
    db = ReconnectMySQLDatabase.get_db_instance(app.config['mysql'])
    db_proxy.initialize(db)
    mgr = Manager(db)
    app.ctx.db = mgr

    # 注册 redis
    app.ctx.redis = await RedisSession.get_redis_pool(app.config['redis'])


@app.after_server_stop
async def stop(app):
    print("app stop")
    await app.ctx.db.close()
    await app.ctx.redis.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8089, debug=app.config['DEBUG'])
