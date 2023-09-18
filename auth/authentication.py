import logging

from fastapi import Request, Depends, HTTPException

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
    async def hmac_auth(cls, request:Request) -> User:
        hm = HmacAuthModule(request)
        user = await hm.authenticate()
        return user



class AuthRoute:
    """Static methods in this class are what actually get called in the "Depends()"
    param of each route. These static methods are the point of entry for our auth module,
    via the routes the user is attempting to access.
    """
    @staticmethod
    async def spider_launch(user: User = Depends(Authenticators.key_auth)) -> User:
        """spider launch endpoint"""
        perm = Authorization()
        await perm.has_permissions(user, perm.STAFF, perm.SPIDERLAUNCH)
        
        return user


    @staticmethod
    async def staff_only(user: User = Depends(Authenticators.key_auth)) -> User:
        """Staff members only"""   
        perm = Authorization()
        await perm.has_permissions(user, perm.STAFF)
        
        return user


    @staticmethod
    async def admin_only(user: User = Depends(Authenticators.key_auth)) -> User:
        """Admin level only"""   
        perm = Authorization()
        await perm.has_permissions(user, perm.ADMIN)
        
        return user


