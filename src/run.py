from sanic import Sanic
from src.config import CONFIG
from werkzeug.utils import find_modules, import_string

app = Sanic(name='async-task')
app.config.update(CONFIG.get_config())


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
async def setup(app, loop):
    print("app start")
    pass


@app.after_server_stop
async def stop(app):
    print("app stop")
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=app.config['DEBUG'])
