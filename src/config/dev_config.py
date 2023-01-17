from .config import Config


class DevConfig(Config):
    DEBUG = True
    ACCESS_LOG = True
    WORKERS = 1

    # 日志配置
    BASE_LOGGING = {
        'version': 1,
        'loggers': {
            "sanic.root": {"level": "INFO", "handlers": ["console"]},
        },
        'formatters': {
            'default': {
                'format': '%(asctime)s | %(levelname)s | %(message)s',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'default',
            }
        }
    }
