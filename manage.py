import asyncio
import peewee
from rich.console import Console
from rich.tree import Tree
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
        'error': "bold red",
        'start': '',
        'done': "bold green"
    }
    console.print(f'【{config_data["PROJECT_NAME"]}】{msg}', style=style[mode])


def tree_log(msg, guide_style='bold bright_blue'):
    return Tree(
        f'【{config_data["PROJECT_NAME"]}】{msg}',
        guide_style=guide_style
    )


async def run():
    await create_table()
    # await role()
    await mgr.close()


async def create_table():
    log("开始创建数据表...")
    models = importlib.import_module('src.models.__init__')
    # 获取该模块配置的所有 model
    gen_model_args = (args for args in models.__dict__
                      if not args.startswith('__'))
    for args in gen_model_args:
        # 获取真实 model 对象
        model = getattr(models, args)
        # 通过子类判断更加合理
        if issubclass(model, peewee.Model):
            MigratorOperate(model)
            log(f"生成表 {model._meta.table_name}")

    log("数据表创建完成!", mode='done')


async def role():
    log("初始化系统默认角色...")
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
    await mgr.execute(
        RoleModel.insert_many(role_list)
    )
    log("系统默认角色创建完成!", mode='done')


def admin():
    log("初始化管理员账号...")
    admin_data = config_data.get('ADMIN', dict(username="admin", password="admin123"))
    salt = gen_random(length=12)
    admin_data['salt'] = salt
    admin_data['password'] = gen_password(admin_data['password'], salt)
    print(admin_data)


if __name__ == '__main__':
    asyncio.run(run())
