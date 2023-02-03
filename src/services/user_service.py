from src.models import UserModel
from src.config.context import Request


async def query_user_by_id(request: Request, user_id: str) -> UserModel:
    user_data_gen = await request.ctx.db.execute(
        UserModel.select().where((UserModel.id == user_id))
    )
    return user_data_gen[0]


async def query_user_by_login(request: Request, data) -> UserModel:
    user_data_gen = await request.ctx.db.execute(
        UserModel.select().where((UserModel.username == data['username']))
    )
    return user_data_gen[0]
