import asyncio
import logging
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

from config import SENTINEL
from webscraping.exceptions import PipelineModuleNotFound
from webscraping.models import SpiderAsset
from webscraping.pipeline import Pipeline
# from webscraping.spider import Spider


logger = logging.getLogger("scraping")


class PipelineListener:
    """This class handles listening to the queue for scraped data, 
    and then passing it to the appropriate Pineline subclass.
    """

    def __init__(self, queue:asyncio.Queue, spiders:list[SpiderAsset]):
        self.queue = queue
        self.sentinel = SENTINEL
        self.spider_registry = self._create_spider_registry(spiders)



    def _create_spider_registry(self, spiders:list[SpiderAsset]) -> dict:
        """Converts the list of SpiderAssets into a dictionary, with each 
        SpiderAsset id being a key for the SpiderAsset.
        This will speed up the time it takes to find a spider via its ID when
        retrieving data from the queue.
        """
        return {spider.id: spider for spider in spiders}


    async def get_spider_asset(self, spider_id:int) -> SpiderAsset:
        """Returns the SpiderAsset from the spider registry"""
        return self.spider_registry[spider_id]


    async def get_pipeline_class(self, sa:SpiderAsset) -> Pipeline | None:
        """Retrieves the pipeline class for the SpiderAsset"""
        return "bleh"



    async def listen(self):
        """Checking the queue for data"""
        # pipeline listener role:
        # listens to the queue for new data
        # data that comes will include the Spider or Pipeline name to identify which pipeline to use.
        # pipeline handler instantiates the proper pipeline, and passes it the spider's data.
        # pipeline object (not handler) has specific logic for that specific spider's data to pass it to DB.

        while True:
            data = await self.queue.get()
            if data == self.sentinel:
                logger.info("Sentinel value received")
                break
            print(data['id'])
            print(self.spider_registry[data['id']].spider_name)
        logger.info("Pipeline terminated")
