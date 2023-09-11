import aiohttp
import asyncio
import importlib
import logging
from concurrent.futures import ThreadPoolExecutor

from common.enums import LogLevel
from config import SPIDER_MODULES
# from .models import SpiderAsset
# from .spider import SpiderModuleNotFound
from webscraping.models import SpiderAsset
from webscraping.exceptions import SpiderModuleNotFound

logger = logging.getLogger("scraping")

class SpiderLauncher:
    """Class From which we launch the spiders asynchronously"""

    modules:str = SPIDER_MODULES

    def __init__(self):
        self.spiders = []
        self.spider_count = 0


    async def initialize(self):
        """Fetch the active SpiderAssets and await them."""
        self.spiders = await SpiderAsset.get_active()
        self.spider_count = len(self.spiders)
        return


    async def launch_spiders(self): 
        """Iterates through all the spiders and calls launch_spider()"""
        # await asyncio.gather(*(self.launch_spider(spider.spider_name) for spider in self.spiders))
        # return

        tasks = []
        tasks = [asyncio.create_task(self.launch_spider(spider.spider_name)) for spider in self.spiders]
        with ThreadPoolExecutor() as executor:

            for spider in self.spiders:
                task = asyncio.create_task(self.launch_spider(spider.spider_name))
                tasks.append(task)
            await asyncio.gather(*tasks)
        # with ThreadPoolExecutor() as executor:
        #     for spider in self.spiders:
        #         task = asyncio.create_task(self.launch_spider(spider.spider_name))
        #         tasks.append(task)
        #     await asyncio.gather(*tasks)

        return


    async def launch_spider(self, spider_name:str):
        """Dynamically import the spider module and instantiate the class
        associated with spider_name. Spiders are configured to run on
        instantiation.
        """
        print('spider name: ', spider_name)
        module_name = f"webscraping.modules.{spider_name.lower()}"
        module = importlib.import_module(module_name)
        try:
            SpiderClass = getattr(module, spider_name)
        except AttributeError as e:
            logger.error(f"{repr(SpiderModuleNotFound(e))}")
            spider = await SpiderAsset.get(spider_name=spider_name)
            await spider.deactivate()
        else:    
            spider = SpiderClass()
            await spider.run()

# async def main():
#     launcher = SpiderLauncher()
#     await launcher.initialize()


# asyncio.run(main())
