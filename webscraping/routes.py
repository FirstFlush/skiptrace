import asyncio
import logging
from fastapi import APIRouter
from .launcher import SpiderLauncher
from .pipeline_listener import PipelineListener
from .models import SpiderAsset#, SpiderError



logger = logging.getLogger('scraping')


router = APIRouter()


@router.get("/")
async def root():

    queue = asyncio.Queue()
    logger.debug('Async Queue object created')
    active_spiders = await SpiderAsset.get_active()
    sl = SpiderLauncher(queue, active_spiders)
    pl = PipelineListener(queue, active_spiders)
    # await sl.initialize()

    logger.debug('Initialized Spider Launcher')
    logger.debug('Initialized Pipeline Listener')

    
    await asyncio.gather(sl.launch(), pl.listen())


    return {"asdffdsa": "fdafdsaf scrapppe"}



@router.get("/get_spiders")
async def get_spiders():

    spiders = await SpiderAsset.all()
    spider = spiders[0]
    errors = await spider.errors()
    error_count = await spider.error_count()
    print(errors)
    print(error_count)

    # await SpiderAsset.create(
    #     spider_name = "FindAGrave"
    # )
    # spiders = await SpiderAsset.all()
    # spider = spiders[0]

    # error = await SpiderError.create(
    #     spider_id = spider,
    #     error = "SpiderHttpError",
    # )
    
    # print(spider)
    # print(error)



    return {"hi":"ho"}