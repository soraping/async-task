import multiprocessing
from .config import Config


class ProConfig(Config):
    DEBUG = False
    ACCESS_LOG = False
    WORKERS = multiprocessing.cpu_count()
