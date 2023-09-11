from __future__ import annotations
from typing import Awaitable, List

from tortoise.models import Model
from tortoise import fields


class SpiderAsset(Model):

    spider_name     = fields.CharField(max_length=255)
    is_active       = fields.BooleanField(default=True)
    date_modified   = fields.DatetimeField(auto_now=True)
    date_created    = fields.DatetimeField(auto_now_add=True)


    async def deactivate(self):
        """Deactivates the spider so it will not be loaded into
        the SpiderLauncher
        """
        self.is_active = False
        await self.save()
        return


    async def errors(self) -> Awaitable[List[SpiderError]]:
        return await self.spider_errors.all()
        

    async def error_count(self) -> int:
        """Get number of errors this spider has generated."""
        return await SpiderError.filter(spider_id=self).count()



    def file_path(self, modules_path:str) -> str:
        """Returns the full file path, assuming the naming convention is:
        Class   SpiderName
        File    spidername.py
        """
        path = f"{modules_path}/{self.spider_name.lower()}.py"
        return path


    @classmethod
    async def get_active(cls) -> Awaitable[List["SpiderAsset"]]:
        """Returns all active Spider assets"""
        spiders = await cls.filter(is_active=True)
        return spiders
    

class SpiderError(Model):

    spider_id = fields.ForeignKeyField('models.SpiderAsset', related_name='spider_errors', on_delete=fields.CASCADE)
    error = fields.CharField(max_length=255)
    date_logged = fields.DatetimeField(auto_now_add=True)