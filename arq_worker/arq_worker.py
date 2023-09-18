from arq import create_pool
from arq.connections import RedisSettings
from tortoise import Tortoise

import asyncio
import logging
from webscraping.launcher import SpiderLauncher
from webscraping.models import SpiderAsset
from webscraping.pipeline_listener import PipelineListener

from main import TORTOISE_ORM


logger = logging.getLogger('scrape')


async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()  # if you need to



async def launch_spiders(ctx):

    queue = asyncio.Queue()
    logger.debug('Async Queue object created')
    active_spiders = await SpiderAsset.get_active()
    sl = SpiderLauncher(queue, active_spiders)
    pl = PipelineListener(queue, active_spiders)

    logger.debug('Initialized Spider Launcher')
    logger.debug('Initialized Pipeline Listener')
    
    await asyncio.gather(sl.launch(), pl.listen())
    return "scraped it in arq or someshit"


async def shutdown(ctx):
    # Close Tortoise-ORM connections.
    await Tortoise.close_connections()


# context = {"db": None}  # You can store shared context here.

worker_settings = {
    "functions": [launch_spiders],  # List of functions to execute.
    "on_startup": init,  # Function to call on startup.
    "on_shutdown": shutdown,  # Function to call on shutdown.
    "redis_settings": RedisSettings(),  # Your Redis connection settings.
    # "ctx": context,  # Context passed to each function.
}

# if __name__ == "__main__":
#     # This will run the Arq worker when this file is executed.
#     from arq.worker import run_worker

#     run_worker(**worker_settings)