from sanic import Sanic, exceptions, Request
from sanic.log import logger
from sanic.response import json


class ConfigurationConflictError(exceptions.SanicException):
    """
    配置异常
    """
    ...


class JWTTokenDecodeError(exceptions.SanicException):
    message = "An error decoding a JWT"


class InvalidJWTTokenError(exceptions.SanicException):
    status_code = 422
    message = "Authorization invalid"


class NoAuthorizationError(exceptions.SanicException):
    """
    token 不存在
    """
    status_code = 401
    message = "header must has authorization"


class InitErrorHandler:

    def __init__(self, code):
        self.code = code

    @classmethod
    def initialize(cls, app: Sanic):
        app.error_handler.add(exceptions.ServerError, cls._handler(exceptions.ServerError.status_code))
        app.error_handler.add(exceptions.NotFound, cls._handler(exceptions.NotFound.status_code))

    @classmethod
    def _handler(cls, code):
        return cls(code)

    def __call__(self, request: Request, error: exceptions.SanicException):
        logger.error(str(error))
        return json({'message': str(error), 'errCode': self.code})
