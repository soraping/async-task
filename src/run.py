from sanic import Sanic, Blueprint
from sanic.log import logger
from sanic_openapi import openapi3_blueprint
# from sanic_session import Session, AIORedisSessionInterface
# from sanic_auth import Auth

from src.config import CONFIG
from src.utils import auto_load_gen

# 配置信息
app_config = CONFIG.get_config()

# 服务
app = Sanic(name='async-task', log_config=app_config['BASE_LOGGING'])
app.config.update(app_config)

# 注册 swagger
app.blueprint(openapi3_blueprint)


def register_blueprints(api_module: str, app: Sanic) -> None:
    """
    自动加载bp
    :param api_module:
    :param app:
    :return:
    """
    modules = auto_load_gen(api_module)
    for module in modules:
        if isinstance(module, Blueprint):
            app.blueprint(module)


register_blueprints('views.__init__', app)


# # session 配置
# session = Session()


@app.after_server_start
async def setup(app: Sanic, loop) -> None:
    logger.info("app start")
    logger.info("swagger: {}/swagger".format(app.serve_location))

    # # 注册 redis
    # redis_pool = RedisSession.get_redis_pool(app.config['redis'])
    # app.ctx.redis = await redis_pool
    # logger.info("redis 连接成功")

    # # auth 配置
    # auth = Auth(app)
    # app.ctx.auth = auth

    # jwt
    # JwtExt.initialize(app)

    # # session
    # session.init_app(app, interface=AIORedisSessionInterface(redis_pool))

    # # 注册 mysql
    # app.ctx.db = InitMysql(app.config['mysql']).mgr()

    #
    # # 注册 mongo
    # app.ctx.mongo = MotorBase(**app.config['mongo']).get_db(app.config['mongo']['database'])
    # logger.info("mongo 连接成功")


@app.after_server_stop
async def stop(app):
    logger.info("app stop")
    # await app.ctx.db.close()
    # await app.ctx.redis.close()
    # await app.ctx.mongo.close()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8089,
        workers=app.config['WORKERS'],
        debug=app.config['DEBUG'],
        access_log=app.config['ACCESS_LOG'])
