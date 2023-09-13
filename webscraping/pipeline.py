import asyncio
import logging
from tortoise.transactions import atomic


logger = logging.getLogger("scraping")


class PipelineHandler:

    def __init__(self, queue:asyncio.Queue()):
        self.queue = queue

    async def listen(self):
        """Checking the queue for data"""
        # pipeline handlers role:
        # listens to the queue for new data
        # data that comes will include the Spider or Pipeline name to identify which pipeline to use.
        # pipeline handler instantiates the proper pipeine, and passes it the spider's data.
        # pipeline object (not handler) has specific logic for that specific spider's data to pass it to DB.
        print('listening to the queue')


class BasePipeline:

    async def process_item(self, item:str):

        return item
    

    async def save_items(self):
        # check if theres 1 entry to save or multiple
        # check if the entries are for 1 table or multiple
        # if multipleentries, make sure they are atomic
        # single entry:

        #   -regular db create
        # multiple entries, single table:
        #   -bulk_create
        # multiple entries, multiple tables:
        #   -mutiple bulk_create

        return