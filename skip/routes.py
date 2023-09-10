from fastapi import APIRouter
from skip.models import Bank, Skip, SkipEmail

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello Derp"}


@router.get("/see")
async def see():
    banks = await Bank.all().delete()
    print(banks)
    # print(banks)


@router.get("/test_data")
async def test():

    skip = await Skip.get(ssn="123456789")

    email = await SkipEmail.create(
        skip_id=skip,
        email="nfdasca",

    )
    print(email.__dict__)
    return {"hi":"ho"}