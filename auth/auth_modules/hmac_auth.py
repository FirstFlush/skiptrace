from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, HTTPDigest

from tortoise.exceptions import DoesNotExist, OperationalError

from auth.exceptions import UserInvalid, UserValidKeyInvalid
from auth.models import User
from auth.auth_base import AuthModuleBase



class HmacAuthModule(AuthModuleBase):
    pass