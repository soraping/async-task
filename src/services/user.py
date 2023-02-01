from sanic import Sanic
from src.models import UserModel


async def query_user_by_id(app: Sanic, user_id: str) -> UserModel:
    user_data_gen = await app.ctx.db.execute(
        UserModel.select().where((UserModel.id == user_id))
    )
    print(user_data_gen)


async def query_user_by_login(app: Sanic, data) -> UserModel:
    user_data_gen = await app.ctx.db.execute(
        UserModel.select().where((UserModel.username == data['username']))
    )
    return user_data_gen[0]
