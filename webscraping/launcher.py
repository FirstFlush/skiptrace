import aiohttp
import asyncio
import config
import importlib

# from .models import SpiderAsset
# from .spider import SpiderModuleNotFound
from webscraping.models import SpiderAsset
from webscraping.err import SpiderModuleNotFound


class SpiderLauncher:
    """Class From which we launch the spiders asynchronously"""

    modules:str = config.SPIDER_MODULES
    
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
        tasks = []
        # tasks = [asyncio.create_task(self.launch_spider(spider.spider_name)) for spider in self.spiders]
        for spider in self.spiders:
            task = asyncio.create_task(self.launch_spider(spider.spider_name))
            tasks.append(task)
        await asyncio.gather(*tasks)

        return


    async def launch_spider(self, spider_name:str):
        """Dynamically import the spider module and instantiate the class
        associated with spider_name. Spiders are configured to run on
        instantiation.
        """
        module_name = f"webscraping.modules.{spider_name.lower()}"
        module = importlib.import_module(module_name)
        try:
            SpiderClass = getattr(module, spider_name)
        except AttributeError:
            # log and deactivate SpiderAsset
            spider = await SpiderAsset.get(spider_name=spider_name)
            spider.deactivate()
        else:    
            spider = SpiderClass()


# async def main():
#     launcher = SpiderLauncher()
#     await launcher.initialize()


# asyncio.run(main())
