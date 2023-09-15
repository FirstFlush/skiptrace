from __future__ import annotations
import asyncio
import logging
from pydantic import BaseModel as PydanticBaseModel
from tortoise.transactions import atomic
from tortoise.models import Model
from webscraping.exceptions import PipelineItemInvalid


logger = logging.getLogger("scraping")


class Pipeline:

    def __init__(self, data:list[dict]):
        self.data = data
        self.tables:list[PydanticBaseModel] = []
        self.processed_data:list[PydanticBaseModel] = []


    def process_data(self):
        """Iterates through each dict in the data list and """

        for item in self.data:

            print(self.data)
            print('*'*50)

            print('ITEM: ', item)
            processed_item = self.process_item(item)
            if item is not None:
                self.processed_data.append(processed_item)
            else:
                logger.error(repr(PipelineItemInvalid(f"{item[:50]}...")))


    def process_item(self, item:dict):
        """Overwrite this subclass with specific Pipeline subclass logic."""
        return item
    

    async def save_data(self):
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