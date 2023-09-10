import asyncio

from fastapi import APIRouter
from .launcher import SpiderLauncher
from .models import SpiderAsset
# from skip.models import Bank


router = APIRouter()


@router.get("/")
async def root():

    sl = SpiderLauncher()
    await sl.initialize()
    
    # for spider in sl.spiders:
    #     print(spider.file_path(sl.modules))

    await sl.launch_spiders()

    return {"asdffdsa": "fdafdsaf scrapppe"}



@router.get("/get_spiders")
async def get_spiders():

    # await SpiderAsset.create(
    #     spider_name = "FindAGrave"
    # )
    spiders = await SpiderAsset.all()
    print(spiders)
    return {"hi":"ho"}