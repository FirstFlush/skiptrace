# from __future__ import annotations
import asyncio
import logging
from datetime import datetime

from config import SENTINEL, ACCEPTABLE_SPIDER_DURATION
from webscraping.models import SpiderAsset, SpiderError
from webscraping.exceptions import BrokenSpidersError


logger = logging.getLogger("scraping")


class SpiderLauncher:
    """Class From which we launch the spiders asynchronously 
    and feed them into the database pipeline.
    """

    def __init__(self, queue:asyncio.Queue, spiders:list[SpiderAsset]):
        self.spiders = spiders
        self.spider_count = len(self.spiders)
        self.broken_spiders:list[tuple] = []
        self.queue = queue
        self.sentinel = SENTINEL


    def broken_spider(self, spider_id:int, error_name:str):
        """When a spider fails, append the spider ID
        to self.broken_spiders
        """
        self.broken_spiders.append((spider_id, error_name))
        return


    async def send_to_queue(self, spider_id:int, data:dict):
        """Pass a spider's scraped data into the asyncio Queue, 
        to be consumed by the PipelineListener
        """
        if bool(data):
            data = {'id':spider_id} | data
            await self.queue.put(data)

        return


    async def close_queue(self):
        """Closes the async Queue by passing in the sentinel value."""
        logger.debug("Sending sentinel value to PipelineListener...")
        await self.queue.put(self.sentinel)


    def record_timing(self, start:datetime):
        """Function displaying how long the spiders took to 
        finish scraping.
        """
        end = datetime.now()
        logger.info(f"{end.strftime('%H:%M:%S.%f')} Scraping complete")
        time_elapsed = end - start
        time_str = f"\033[1m{time_elapsed}\033[0m to complete"
        if time_elapsed.seconds < ACCEPTABLE_SPIDER_DURATION:
            logger.info(time_str)
        else:
            logger.warning(time_str)
        return


    async def launch(self): 
        """Iterates through all the spiders and calls launch_spider()"""
        tasks = []
        start_time = datetime.now()
        logger.info(f"{start_time.strftime('%H:%M:%S.%f')} Launching {len(self.spiders)} spiders...")
        for spider in self.spiders:
            task = asyncio.create_task(self.launch_spider(spider))
            logger.debug(f"-{spider.spider_name} launched")
            tasks.append(task)
        await asyncio.gather(*tasks)
        await self.close_queue()
        self.record_timing(start_time)
        if len(self.broken_spiders) > 0:
            self.log_errors()
            await self.record_errors()
        else:
            logger.info(f"Broken spiders: 0")

        return


    async def launch_spider(self, sa:SpiderAsset):
        """Dynamically import the spider module and instantiate the class
        associated with spider_name. Spiders are configured to run on
        instantiation.
        """
        SpiderClass = sa.get_spider()
        if SpiderClass is not None:
            spider = SpiderClass()
            async for scraped_data in spider.run():
                await self.send_to_queue(spider_id=sa.id, data=scraped_data)
            await spider.close_session()
            if spider.is_error == True:
                self.broken_spider(sa.id, spider.error)
                logger.error(f"\033[1mBROKEN SPIDER\033[0m - {sa.spider_name}")
        # else:
        #     logger.error(f"{repr(SpiderModuleNotFound(sa.spider_name))}")
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
        spider_errors = [SpiderError(spider_id_id=spider_id, error=error.__class__.__name__) for spider_id, error in self.broken_spiders]
        await SpiderError.bulk_create(spider_errors)
        return


