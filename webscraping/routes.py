import asyncio
import logging
from fastapi import APIRouter, Depends

from auth.authentication import AuthRoute
from auth.models import User

from webscraping.launcher import SpiderLauncher
from webscraping.pipeline_listener import PipelineListener
from webscraping.models import SpiderAsset
from webscraping.schema.pydantic_models import SpiderSchema


logger = logging.getLogger('scraping')


router = APIRouter()


@router.post("/launch")
async def launch_spiders(user:User = Depends((AuthRoute.spider_launch))):

    queue = asyncio.Queue()
    logger.debug('Async Queue object created')
    active_spiders = await SpiderAsset.get_active()
    sl = SpiderLauncher(queue, active_spiders)
    pl = PipelineListener(queue, active_spiders)

    logger.debug('Initialized Spider Launcher')
    logger.debug('Initialized Pipeline Listener')
    
    await asyncio.gather(sl.launch(), pl.listen())

    return {"asdffdsa": "fdafdsaf scrapppe"}



@router.get("/listSpiders")
async def all_spiders():
    spiders = await SpiderAsset.all()
    return [SpiderSchema(spider_name=spider.spider_name, is_active=spider.is_active, description=spider.description) for spider in spiders]


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