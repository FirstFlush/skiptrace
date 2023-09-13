from __future__ import annotations
import importlib
from typing import Awaitable, List

from tortoise.models import Model
from tortoise import fields

from common.fields import URLField
from config import SPIDER_MODULES, PIPELINE_MODULES
from webscraping.pipeline import Pipeline
from webscraping.spider import Spider
from webscraping.exceptions import SpiderModuleNotFound, PipelineModuleNotFound


class SpiderAsset(Model):

    spider_name     = fields.CharField(max_length=255)
    # domain          = fields.URLField(max_length=255)
    is_active       = fields.BooleanField(default=True)
    date_modified   = fields.DatetimeField(auto_now=True)
    date_created    = fields.DatetimeField(auto_now_add=True)


    def get_spider(self) -> Spider | None:
        """Retrieve the Spider subclass, based on naming convention."""
        # module_name = f"webscraping.modules.spiders.{self.spider_name.lower()}"
        module_name = f"{SPIDER_MODULES}.{self.spider_name.lower()}"
        module = importlib.import_module(module_name)
        try:
            SpiderClass = getattr(module, f"{self.spider_name}Spider")
        except AttributeError:
            SpiderClass = None

        return SpiderClass


    def get_pipeline(self) -> Pipeline | None:
        """Retrieve the Pipeline subclass, based on naming convention."""
        module_name = f"webscraping.modules.pipelines.{self.spider_name.lower()}"
        module = importlib.import_module(module_name)
        try:
            PipelineClass = getattr(module, f"{self.spider_name}Pipeline")
        except AttributeError:
            PipelineClass = None

        return PipelineClass



    async def activate(self):
        """Activates the spider so it will be loaded into
        the SpiderLauncher
        """
        self.is_active = True
        await self.save()
        return


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