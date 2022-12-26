from sanic import response, Blueprint

bp = Blueprint('goods', url_prefix='/goods')


@bp.get('/list')
async def get_goods_list(request):
    return response.json({"goods_list": [1, 2, 3]})
