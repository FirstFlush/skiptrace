import asyncio

from fastapi import APIRouter
from .launcher import SpiderLauncher
from .models import SpiderAsset, SpiderError
# from skip.models import Bank


router = APIRouter()


@router.get("/")
async def root():

    sl = SpiderLauncher()
    await sl.initialize()
    await sl.launch()

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