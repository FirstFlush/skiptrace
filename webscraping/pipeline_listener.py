import asyncio
import logging
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

from config import SENTINEL
# from webscraping.exceptions import PipelineModuleNotFound
from webscraping.models import SpiderAsset
from webscraping.pipeline_base import Pipeline
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

        exmaple: {2:WebsiteAbcSpider, 3:WebsiteXyzSpider}
        """
        return {spider.id: spider for spider in spiders}


    def get_spider_asset(self, spider_id:int) -> SpiderAsset:
        """Returns the SpiderAsset from the spider registry"""
        return self.spider_registry[spider_id]


    def get_pipeline_object(self, sa:SpiderAsset, scraped_data:list[dict]) -> Pipeline | None:
        """Retrieves the pipeline class for the SpiderAsset"""
        pipeline = None
        PipelineClass = sa.get_pipeline()
        if PipelineClass is not None:
            pipeline = PipelineClass(scraped_data)
        return pipeline


    async def listen(self):
        """Checking the queue for data and instantiating the 
        appropriate Pipeline subclass.
        """
        while True:
            data = await self.queue.get()
            if data == self.sentinel:
                logger.info("Pipeline sentinel value received")
                break
            spider_asset = self.spider_registry[data['id']]
            pipeline = self.get_pipeline_object(spider_asset, data)
            if pipeline is not None:
                pipeline.process_data()

        logger.info("Pipeline terminated")
