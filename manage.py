import asyncio
import click
from src.config import CONFIG
from src.extension import init_mysql
from src.models import RoleTypeEnum, RoleModel, UserModel
from src.utils import gen_random, gen_password

config_data = CONFIG.get_config()
mgr = init_mysql(config_data['mysql'])


async def run():
    await role()


async def role():
    print("初始化系统默认角色...")
    role_list = [
        {
            "name": "管理员",
            "type": RoleTypeEnum.ADMIN.value
        },
        {
            "name": "客户",
            "type": RoleTypeEnum.NORMAL.value
        }
    ]

    try:
        await mgr.execute(RoleModel.select())
    except Exception as ex:
        print(ex)


def admin():
    print("初始化管理员账号...")
    admin_data = config_data.get('ADMIN', dict(username="admin", password="admin123"))
    salt = gen_random(length=12)
    admin_data['salt'] = salt
    admin_data['password'] = gen_password(admin_data['password'], salt)
    print(admin_data)


if __name__ == '__main__':
    asyncio.run(run())
