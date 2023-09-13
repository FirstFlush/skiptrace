import asyncio
import logging
from fastapi import APIRouter
from .launcher import SpiderLauncher
from .pipeline import PipelineHandler
from .models import SpiderAsset, SpiderError
# from skip.models import Bank


logger = logging.getLogger('scraping')


router = APIRouter()


@router.get("/")
async def root():

    queue = asyncio.Queue()
    sl = SpiderLauncher(queue)
    ph = PipelineHandler(queue)
    logger.debug('Initializing Pipeline Handler')
    await sl.initialize()
    logger.debug('Initialized Spider Launcher')

    
    await asyncio.gather(sl.launch(),ph.listen())

    # await sl.launch()



    # print()
    # print("broken spiders: ", sl.broken_spiders)

    # print()
    # se = await SpiderError().all()
    # print(se)
    # print(len(se))
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