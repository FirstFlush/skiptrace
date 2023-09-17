from __future__ import annotations
import bcrypt
import secrets
import uuid
from tortoise.models import Model
from tortoise import fields

# from auth.modules.api_key_auth import ApiKeyAuthModule

from common.fields import EmailField


class User(Model):
    """api_key is stored as a bcrypt hash."""

    access_id       = fields.UUIDField(index=True, max_length=36, unique=True, default=uuid.uuid4)
    email           = EmailField(max_length=255, unique=True)
    permissions     = fields.ManyToManyField("models.Permission", related_name="user")
    api_key         = fields.CharField(max_length=128, unique=True)
    is_active       = fields.BooleanField(default=True)
    is_staff        = fields.BooleanField(default=False)
    is_admin        = fields.BooleanField(default=False)
    date_created    = fields.DatetimeField(auto_now_add=True)


    @classmethod
    async def create_new_user(cls, email:str, key:str=None,is_staff:bool=False,is_admin:bool=False) -> User:
        new_user = await cls.create(
            email = email,
            api_key= cls.create_user_key() if key is None else key,
            is_staff=is_staff,
            is_admin=is_admin
        )
        return new_user


    @staticmethod
    def _generate_api_key() -> str:
        return secrets.token_urlsafe(64)
    
    @classmethod
    def hash_api_key(cls, api_key:str) -> bytes:
        return bcrypt.hashpw(api_key.encode('utf-8'), bcrypt.gensalt())
    
    @classmethod
    def create_user_key(cls) -> str:
        """Returns a bcrypt-hashed-and-salted API key to store in the DB."""
        key = cls._generate_api_key()
        return cls.hash_api_key(key).decode('utf-8')



class Permission(Model):
    
    perm            = fields.CharField(unique=True, index=True, max_length=64)
    description     = fields.TextField(max_length=2048, null=True)
    date_created    = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.perm