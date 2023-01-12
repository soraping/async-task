import functools


def singleton(cls):
    """
    单例
    :param cls:
    :return:
    """
    _instances = {}

    @functools.wraps(cls)
    def instance(*args, **kw):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kw)
        return _instances[cls]

    return instance