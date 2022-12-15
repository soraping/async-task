import os


class Config:
    TIMEZONE = 'Asia/Shanghai'
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    def __new__(cls, *args, **kwargs):
        """
        修改实例，为app.config.update实际参数
        遍历实例参数，子类属性也会遍历
        :param args:
        :param kwargs:
        """
        return {attr: getattr(cls, attr) for attr in dir(cls) if not attr.startswith("__")}


if __name__ == '__main__':
    print(Config())