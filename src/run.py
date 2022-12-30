from sanic import Sanic
from peewee_async import Manager
from sanic_openapi import openapi3_blueprint
from src.config import CONFIG
from werkzeug.utils import find_modules, import_string
from models import ReconnectMySQLDatabase, db as db_proxy

app = Sanic(name='async-task')
app.config.update(CONFIG.get_config())

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
    db = ReconnectMySQLDatabase.get_db_instance(app.config['mysql'])
    db_proxy.initialize(db)
    mgr = Manager(db)
    app.ctx.db = mgr


@app.after_server_stop
async def stop(app):
    print("app stop")
    await app.ctx.db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=app.config['DEBUG'])
