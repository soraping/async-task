from .config import Config


class DevConfig(Config):
    DEBUG = True
    ACCESS_LOG = True
    WORKERS = 1
