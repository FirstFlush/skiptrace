from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, HTTPDigest


class HmacAuthModule:
    pass