# from __future__ import annotations
import bcrypt
import logging
import secrets

from fastapi import HTTPException

from tortoise.exceptions import DoesNotExist, OperationalError

from auth.auth_module_base import AuthModuleBase
from auth.exceptions import UserInvalid, UserValidKeyInvalid
from auth.models import User


logger = logging.getLogger('auth')


class ApiKeyAuthModule(AuthModuleBase):
    """Basic API key style authentication where user must pass 
    in valid data for both "X-ACCESS and X-API-KEY headers in order 
    to successfully authenticate.
    """

    async def authenticate(self) -> User:
        access_id = self.request.headers.get("X-ACCESS")
        api_key = self.request.headers.get("X-API-KEY")
        if access_id is None or api_key is None:
            self.deny()
        try:
            user = await User.get(access_id=access_id) 
        except (DoesNotExist, OperationalError):
            logger.error(repr(UserInvalid(f"Invalid Access ID: {access_id}")))
            self.deny()
        else:
            if self.verify_api_key(api_key, user.api_key) is False:
                logger.error(repr(UserValidKeyInvalid(f"Access ID: {access_id}")))
                self.deny()
            else:
                return user


    def verify_api_key(self, api_key:str, hashed_api_key:str) -> bool:
        """Compare the user-submitted key with the hash we have in storage."""
        return bcrypt.checkpw(api_key.encode('utf-8'), hashed_api_key.encode('utf-8'))



    

    # def _is_ipython(self) -> bool:
    #     """Print the secret key to the terminal ONLY if we 
    #     are running in an iPython shell.
    #     """
    #     try:
    #         get_ipython
    #     except NameError:
    #         return False
    #     else:
    #         return True

