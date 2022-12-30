from sanic import response, Blueprint
from sanic_openapi import openapi

bp = Blueprint('user', url_prefix='/user')


@bp.get('/list')
@openapi.summary('user list')
async def get_user_list(request):
    return response.json({"msg": "hello world"})
