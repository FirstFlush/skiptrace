from fastapi import APIRouter
# from skip.models import Bank

router = APIRouter()

@router.get("/")
async def root():
    return {"asdffdsa": "fdafdsaf scrapppe"}


# @router_skip.get("/test")
# async def test():
#     bank = await Bank.create(name="test_bank")
#     print(bank)
#     return {"hi":"ho"}