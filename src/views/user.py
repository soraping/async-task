from sanic import response, Blueprint

user_bp = Blueprint('user', url_prefix='/user')


@user_bp.get('/list')
async def get_user_list(request):
    return response.json({"msg": "hello world"})
