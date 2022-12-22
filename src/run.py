from sanic import Sanic
from src.config import CONFIG
from views.user import user_bp

app = Sanic(name='async-task')
app.config.update(CONFIG.get_config())

app.blueprint(user_bp)


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
