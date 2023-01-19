from enum import Enum
from datetime import timedelta
from sanic_jwt_extended import JWT
from sanic_jwt_extended.tokens import Token


class Role(Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'


class JwtExt:
    """
    sanic_jwt_extended
    https://sanic-jwt-extended.seonghyeon.dev/
    https://github.com/NovemberOscar/Sanic-JWT-Extended
    """

    @classmethod
    def initialize(cls, app):
        jwt_config = app.config['JWT']
        with JWT.initialize(app) as manager:
            manager.config.secret_key = str(jwt_config['secret_key']).encode('utf-8')
            manager.config.private_claim_prefix = jwt_config['private_claim_prefix']
            manager.config.access_token_expires = timedelta(days=jwt_config['access_token_expires'])

    @classmethod
    def gen_token(cls, identity, claim):
        return JWT.create_access_token(identity=identity, private_claims=claim)

    @classmethod
    def refresh_token(cls, identity, claim):
        return JWT.create_refresh_token(identity=identity, private_claims=claim)

    @classmethod
    def resolve_token(cls, token):
        """
        检测token
        :param token:
        :return:
        """
        return Token(token)


if __name__ == '__main__':
    ...
