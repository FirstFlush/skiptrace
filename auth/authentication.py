import logging

from fastapi import Request, Depends, HTTPException
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# from tortoise.exceptions import DoesNotExist, OperationalError

# from .exceptions import UserInvalid, UserValidKeyInvalid
from auth.auth_modules.api_key_auth import ApiKeyAuthModule
from auth.authorization import Authorization
from auth.auth_modules.hmac_auth import HmacAuthModule
from auth.models import User


logger = logging.getLogger('auth')


class Authenticators:

    @classmethod
    async def key_auth(cls, request:Request) -> User:
        akm = ApiKeyAuthModule(request)
        user = await akm.authenticate()
        return user


    @classmethod
    def hmac_auth(cls, request:Request) -> bool:
        hm = HmacAuthModule
        # TODO: do stuff here
        return



class AuthRoute:
    
    @staticmethod
    async def spider_launch(user: User = Depends(Authenticators.key_auth)) -> User:
        """spider launch endpoint"""
        perm = Authorization()
        await perm.has_permissions(user, perm.Staff, perm.SpiderLaunch)
        
        return user


    @staticmethod
    async def staff_only(user: User = Depends(Authenticators.key_auth)) -> User:
        """Staff members only"""   
        perm = Authorization()
        await perm.has_permissions(user, perm.Staff)
        
        return user


    @staticmethod
    async def admin_only(user: User = Depends(Authenticators.key_auth)) -> User:
        """Admin level only"""   
        perm = Authorization()
        await perm.has_permissions(user, perm.Admin)
        
        return user


