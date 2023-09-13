import asyncio
import logging
from tortoise.transactions import atomic


logger = logging.getLogger("scraping")


class Pipeline:

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