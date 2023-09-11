# File for storing custom Tortoise-ORM Model fields

from fastapi import HTTPException
from tortoise import fields
import validators


# Custom model fields
# =========================================

class URLField(fields.CharField):

    def to_db_value(self, value: str, instance) -> str:
        # You can add URL validation logic here, for instance:
        if value and not validators.url(value):
            raise HTTPException(422, f"'{value}' is not a valid URL")
        return super().to_db_value(value, instance)
    
    def to_python_value(self, value: str) -> str:
        # You can add URL validation logic here as well, or any other processing you'd like.
        return super().to_python_value(value)
    

class EmailField(fields.CharField):
    def to_db_value(self, value: str, instance) -> str:
        # You can add URL validation logic here, for instance:
        if value and not validators.email(value):
            raise HTTPException(422, f"'{value}' is not a valid email")
        return super().to_db_value(value, instance)
    
    def to_python_value(self, value: str) -> str:
        # You can add URL validation logic here as well, or any other processing you'd like.
        return super().to_python_value(value)
    