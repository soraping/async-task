from sanic import response, Blueprint
from sanic_openapi import openapi
from src.extension import JwtExt

bp = Blueprint('user', url_prefix='/user')


@bp.get('/list')
@openapi.summary('user list')
async def get_user_list(request):
    return response.json({"msg": "hello world"})


@bp.get('/token')
@openapi.summary('user token')
async def get_token(request):
    token = JwtExt.gen_token("123", {"name": "zhangsan"})
    return response.json({"token": token})


@bp.get('/info')
@openapi.summary('user info')
async def get_user(request):
    token = request.args.get('token')

    return response.json({"token": JwtExt.resolve_token(token)})