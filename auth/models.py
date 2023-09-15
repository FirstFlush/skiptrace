from __future__ import annotations
import uuid
from tortoise.models import Model
from tortoise import fields

from auth.modules.api_key_auth import ApiKeyAuthModule

from common.fields import EmailField


class User(Model):
    """api_key is stored as a bcrypt hash."""

    access_id = fields.UUIDField(index=True, max_length=36, unique=True, default=uuid.uuid4)
    email = EmailField(max_length=255, unique=True)
    api_key = fields.CharField(max_length=128, unique=True)
    is_active = fields.BooleanField(default=True)
    is_staff = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)
    date_created = fields.DatetimeField(auto_now_add=True)


    @classmethod
    async def create_new_user(cls, email:str, key:str=None,is_staff:bool=False,is_admin:bool=False) -> User:
        new_user = await cls.create(
            email = email,
            api_key= ApiKeyAuthModule.create_user_key() if key is None else key,
            is_staff=is_staff,
            is_admin=is_admin
        )
        return new_user