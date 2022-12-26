from sanic import response, Blueprint

bp = Blueprint('user', url_prefix='/user')


@bp.get('/list')
async def get_user_list(request):
    return response.json({"msg": "hello world"})
