import os
from enum import Enum


class ModeEnum(Enum):
    DEV = 'DEV'
    PRO = 'PRO'

    @classmethod
    def __missing__(cls, value):
        for mode in cls:
            if mode.value == value.upper():
                return mode


def load_config():
    mode = os.environ.get('MODE', ModeEnum.DEV.value)

    try:
        if mode == ModeEnum.PRO.value:
            from .pro_config import ProConfig
            return ProConfig
        else:
            from .dev_config import DevConfig
            return DevConfig

    except ImportError:
        from .config import Config
        return Config


CONFIG = load_config()
