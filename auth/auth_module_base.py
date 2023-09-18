import logging
from fastapi import Request, Depends, HTTPException
from auth.exceptions import AuthModuleNotFound
# from auth.models import User


logger = logging.getLogger('auth')


class AuthModuleBase:

    def __init__(self, request:Request):
        self.request = request


    async def authenticate(self):
        """Overwrite this method for custom authentication logic 
        for each AuthModule
        """
        logger.error(repr(AuthModuleNotFound(self.__class__.__name__)))
        raise HTTPException(status_code=401, detail="Access denied")
        

    def deny(self, message:str="Access denied"):
        raise HTTPException(status_code=401, detail=message)