from sanic import response, Blueprint, Request
from sanic_openapi import openapi
from src.extension import JwtExt

bp = Blueprint('user', url_prefix='/user')


@bp.post('/login')
@openapi.summary('user login')
async def user_login(request: Request):
    body = request.json
    token = JwtExt.gen_token("c123123", body)
    result = dict(**body, **dict(token=token))
    return response.json({"data": result})


@bp.post('/register')
@openapi.summary('user register')
async def user_register(request: Request):
    body = request.json
    token = JwtExt.gen_token("c123123", body)
    result = dict(**body, **dict(token=token))
    return response.json({"data": result})


@bp.get('/list')
@openapi.summary('user list')
async def get_user_list(request):
    return response.json({"msg": "hello world"})

# @bp.get('/token')
# @openapi.summary('user token')
# async def get_token(request):
#     token = JwtExt.gen_token("123", {"name": "zhangsan"})
#     return response.json({"token": token})
#
#
# @bp.get('/info')
# @openapi.summary('user info')
# async def get_user(request):
#     token = request.args.get('token')
#
#     return response.json({"token": JwtExt.resolve_token(token)})
