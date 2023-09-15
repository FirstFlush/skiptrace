import logging

from fastapi import Request, HTTPException
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from tortoise.exceptions import DoesNotExist, OperationalError

from .exceptions import UserInvalidKeyInvalid, UserValidKeyInvalid
from .modules.api_key_auth import ApiKeyAuthModule
from .modules.hmac_auth import HmacAuthModule
from .models import User


logger = logging.getLogger('auth')


class Authenticators:

    @classmethod
    async def key_auth(cls, request:Request) -> User:
        access_id = request.headers.get("X-ACCESS")
        api_key = request.headers.get("X-API-KEY")
        if access_id is None or api_key is None:
            cls.deny()
        ak = ApiKeyAuthModule()
        try:
            user = await User.get(access_id=access_id) 
        except (DoesNotExist, OperationalError):
            logger.error(repr(UserInvalidKeyInvalid(f"Access ID: {access_id}")))
            cls.deny()
        else:
            if ak.verify_api_key(api_key, user.api_key) is False:
                logger.error(repr(UserValidKeyInvalid(f"Access ID: {access_id}")))
                cls.deny()
            else:
                return user


    @classmethod
    def hmac_auth(cls, request:Request) -> bool:
        pass





    @staticmethod
    def deny(message:str="Access denied"):
        raise HTTPException(status_code=401, detail=message)
