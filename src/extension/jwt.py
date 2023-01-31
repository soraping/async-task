from sanic import Request
from sanic_jwt import exceptions


async def jwt_authenticate(request: Request, *args, **kwargs):
    login_body = request.json
    username = login_body.get('username', None)
    password = login_body.get('password', None)

    if not username or not password:
        raise exceptions.AuthenticationFailed('用户名密码不能为空')


class JwtExt:
    ...
