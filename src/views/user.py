from sanic import Blueprint
from sanic_openapi import openapi
from src.extension import JwtExt
from src.services import user_service
from src.utils import request_log
from src.config.context import Request
from src.models import RoleTypeEnum

user_bp = Blueprint('user', url_prefix='/user')


@user_bp.post('/login')
@openapi.summary('user login')
async def user_login(request: Request):
    body = request.json
    user_data = await user_service.query_user_by_login(request, body)
    token = JwtExt.create_access_token(user_data.id, {'role': user_data.role.type, 'user_id': user_data.id})
    result = dict(**body, **dict(token=token))
    return result


@user_bp.get('/detail')
@openapi.summary('user detail')
@JwtExt.login_required()
async def user_data(request: Request):
    login_data = request.ctx.auth_user
    return {"data": login_data}


@user_bp.get('/info/<user_id>')
@openapi.summary('user info')
@JwtExt.login_required()
@JwtExt.scopes([RoleTypeEnum.ADMIN.value])
@request_log
async def user_data(request: Request, user_id: str):
    login_data = request.ctx.auth_user
    return login_data


# @user_bp.post('/register')
# @openapi.summary('user register')
# async def user_register(request: Request):
#     body = request.json
#     token = JwtExt.gen_token("c123123", body)
#     result = dict(**body, **dict(token=token))
#     return response.json({"data": result})


@user_bp.get('/list')
@openapi.summary('user list')
async def get_user_list(request):
    return {"msg": "hello world"}
