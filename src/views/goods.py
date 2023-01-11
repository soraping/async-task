from sanic import response, Blueprint

bp = Blueprint('goods', url_prefix='/goods')


@bp.get('/list')
async def get_goods_list(request):
    await request.app.ctx.redis.set('name', 'zhangsan')
    name = await request.app.ctx.redis.get('name')
    return response.json({"goods_list": [1, 2, 3]})
