import asyncio
from rich.console import Console
import importlib
from src.config import CONFIG
from src.extension import InitMysql
from migrations import MigratorOperate
from src.models import RoleTypeEnum, RoleModel, UserModel
from src.utils import gen_random, gen_password

config_data = CONFIG.get_config()
mgr = InitMysql(config_data['mysql']).mgr()

console = Console()


def log(msg, mode='info'):
    style = {
        'info': "bold blue",
        'warn': "bold yellow",
        'error': "bold red"
    }
    console.print(f'【{config_data["PROJECT_NAME"]}】{msg}', style=style[mode])


async def run():
    await create_table()


async def create_table():
    log("开始创建数据表...")
    models = importlib.import_module('src.models.__init__')
    # 获取该模块配置的所有 model
    gen_model_args = (args for args in models.__dict__
                      if not args.startswith('__') and args.__contains__('Model'))
    for args in gen_model_args:
        # 获取真实 model 对象
        model = getattr(models, args)
        MigratorOperate(model)
        log(f"生成表 {args}")





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
        # await mgr.execute(
        #     RoleModel.insert_many(role_list)
        # )

        roles = await mgr.execute(RoleModel.select())
        print(list(roles))
        await mgr.close()

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
