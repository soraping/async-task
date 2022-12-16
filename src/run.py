from sanic import Sanic
from sanic import response
from src.config import CONFIG

app = Sanic(name='async-task')
app.config.update(CONFIG.get_config())


@app.route('/hello')
async def hello(request):
    return response.text('hello world!')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=app.config['DEBUG'])
