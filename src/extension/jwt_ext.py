from dataclasses import dataclass
from typing import List, Optional, Union, Dict
from datetime import timedelta, datetime, timezone
from contextlib import contextmanager
from functools import wraps
from sanic import Sanic, Request
from sanic.log import logger
import jwt
from src.utils.exceptions import (
    InvalidJWTTokenError,
    ConfigurationConflictError,
    JWTTokenDecodeError,
    NoAuthorizationError
)
from src.utils import json_prettify


@dataclass
class Claim:
    role: str
    user_id: str


@dataclass
class JwtConfig:
    secret_key: Optional[str] = None
    # token 过期时间
    access_token_expires: Union[timedelta, bool] = timedelta(days=1)
    algorithm: str = "HS256"


class JwtExt:
    config = None
    _cache = None

    @classmethod
    @contextmanager
    def initialize(cls, app: Sanic):
        cls.config = JwtConfig()
        yield JwtExt
        cls._validate_config()

    @classmethod
    def create_access_token(cls, identity: str, claim: Dict[str, str]) -> str:
        return jwt.encode(
            dict(
                # 过期时间
                exp=datetime.now() + cls.config.access_token_expires,
                # 签发时间
                iat=int(datetime.now(tz=timezone.utc).timestamp()),
                # 签发人
                iss=identity,
                data=claim
            ),
            cls.config.secret_key,
            algorithm=cls.config.algorithm
        )

    @classmethod
    def check_token(cls, auth_token: str):
        try:
            cls.resolve_token(auth_token)
        except jwt.exceptions.InvalidTokenError:
            return False
        finally:
            return True

    @classmethod
    def resolve_token(cls, auth_token: str):
        try:
            jwt_data = jwt.decode(
                auth_token,
                cls.config.secret_key,
                algorithms=[cls.config.algorithm]
            )
            return jwt_data['data']
        except jwt.exceptions.DecodeError:
            raise JWTTokenDecodeError

    @classmethod
    def login_required(cls):
        def decorator(func):
            @wraps(func)
            async def decorated_function(request: Request, *args, **kwargs):
                auth_token = request.headers.get('Authorization')
                if not cls.check_token(auth_token):
                    raise InvalidJWTTokenError
                resolve_token_data = cls.resolve_token(auth_token)
                request.app.ctx.login_user = resolve_token_data
                logger.info(f"request_id={str(request.id)}\nlogin_user={json_prettify(resolve_token_data)}")
                response = await func(request, *args, **kwargs)
                return response

            return decorated_function

        return decorator

    @classmethod
    def scopes(cls, scopes: List[str]):
        ...

    @classmethod
    def _validate_config(cls):
        """
        校验 jwt config
        :return:
        """
        if not cls.config.secret_key:
            raise ConfigurationConflictError("You should config secret_key to string!")

    @classmethod
    async def _check_token_cache(cls, identity: str):
        """
        检验并返回token
        :param identity:
        :return:
        """
        if cls._cache:
            cache_token = await cls._cache.get(identity)
            if not cache_token:
                raise NoAuthorizationError
            return cache_token

    @classmethod
    async def _save_token_cache(cls, identity: str, auth_token: str):
        """
        缓存token
        :param identity:
        :param auth_token:
        :return:
        """
        if cls._cache:
            await cls._cache.set(identity, auth_token)


if __name__ == '__main__':
    with JwtExt.initialize(Sanic('test1')) as manager:
        manager.config.secret_key = "test1"
        manager.config.access_token_expires = timedelta(minutes=1)

    token = JwtExt.create_access_token("zhangsan", dict(role='admin', user_id='12321'))
    print('token =>', token)
    data = JwtExt.resolve_token(token)
    print('data => ', data)
