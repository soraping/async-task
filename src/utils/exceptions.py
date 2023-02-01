from sanic import exceptions, Request
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
    message = "Authorization invalid"


class ErrorHandler:

    def __init__(self, code):
        self.code = code

    def __call__(self, request: Request, error: exceptions.SanicException):
        return json({'message': str(error), 'errCode': self.code})
