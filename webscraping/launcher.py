import aiohttp
import asyncio
import importlib
import logging
import time

from common.enums import LogLevel
from config import SPIDER_MODULES
# from .models import SpiderAsset
# from .spider import SpiderModuleNotFound
from webscraping.models import SpiderAsset, SpiderError
from webscraping.exceptions import SpiderModuleNotFound, BrokenSpidersError

logger = logging.getLogger("scraping")

class SpiderLauncher:
    """Class From which we launch the spiders asynchronously"""

    modules:str = SPIDER_MODULES

    def __init__(self):
        self.spiders = []
        self.spider_count = 0
        self.broken_spiders:list[tuple] = []


    async def initialize(self):
        """Fetch the active SpiderAssets and await them."""
        self.spiders = await SpiderAsset.get_active()
        self.spider_count = len(self.spiders)
        return


    def broken_spider(self, spider_id:int, error_name:str):
        """When a spider fails, append the spider ID
        to self.broken_spiders
        """
        self.broken_spiders.append((spider_id, error_name))
        return


    async def launch(self): 
        """Iterates through all the spiders and calls launch_spider()"""
        tasks = []
        logger.critical('blehh')
        logger.info(f"Launching {len(self.spiders)} spiders...")
        for spider in self.spiders:
            logger.debug(spider.spider_name)
            task = asyncio.create_task(self.launch_spider(spider))
            tasks.append(task)
        await asyncio.gather(*tasks)
        
        logger.info("All spiders have returned")
        logger.info(f"Broken spiders: {len(self.broken_spiders)}")
        if len(self.broken_spiders) > 0:
            self.log_errors()
            await self.record_errors()

        return


    async def launch_spider(self, sa:SpiderAsset):
        """Dynamically import the spider module and instantiate the class
        associated with spider_name. Spiders are configured to run on
        instantiation.
        """
        # print('Starting:    ', sa.spider_name)
        module_name = f"webscraping.modules.{sa.spider_name.lower()}"
        module = importlib.import_module(module_name)
        try:
            SpiderClass = getattr(module, sa.spider_name)
        except AttributeError as e:
            logger.error(f"{repr(SpiderModuleNotFound(e))}")
            self.broken_spider(sa.id, SpiderModuleNotFound)
        else:    
            spider = SpiderClass()
            await spider.run()
            # print('--------------------')
            # print(sa.spider_name)
            # print(spider.__dict__)
            # print()
            if spider.is_error == True:
                self.broken_spider(sa.id, spider.error)
        return


    def log_errors(self):
        """Creates a BrokenSpiders log entry"""
        num = len(self.broken_spiders)
        logger.error(repr(BrokenSpidersError(f"{num} broken spider{'' if num==1 else 's'}")))
        return
    

    async def record_errors(self):
        """Creates a SpiderError object in the DB for each of 
        the spiders in self.broken_spiders
        """
        # print('record: ', self.broken_spiders)
        spider_errors = [SpiderError(spider_id_id=spider_id, error=error.__class__.__name__) for spider_id, error in self.broken_spiders]
        await SpiderError.bulk_create(spider_errors)
        return


