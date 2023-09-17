from fastapi import Request, Depends, HTTPException
from auth.models import User


class AuthModuleBase:

    def __init__(self, request:Request):
        self.request = request


    async def authenticate(self):
        """Overwrite this method for custom authentication logic 
        for each AuthModule
        """
        return


    def deny(self, message:str="Access denied"):
        raise HTTPException(status_code=401, detail=message)