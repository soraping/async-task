import os
import types


class Config:
    TIMEZONE = 'Asia/Shanghai'
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    @classmethod
    def get_config(cls):
        """
        修改实例，为app.config.update实际参数
        遍历实例参数，子类属性也会遍历
        """
        # 去掉method
        attr_gen = (i for i in dir(cls) if type(getattr(cls, i)) is not types.MethodType)
        return {
                    attr: getattr(cls, attr)
                    for attr in attr_gen
                    if not attr.startswith('__')
        }

    # def __new__(cls, *args, **kwargs):
    #     """
    #     修改实例，为app.config.update实际参数
    #     遍历实例参数，子类属性也会遍历
    #     :param args:
    #     :param kwargs:
    #     """
    #     return {attr: getattr(cls, attr) for attr in dir(cls) if not attr.startswith("__")}


if __name__ == '__main__':
    print(Config.get_config())