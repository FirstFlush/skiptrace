import logging
from fastapi import APIRouter, Depends#, HTTPException

from .authentication import AuthRoute
from .models import User


logger = logging.getLogger('auth')
router = APIRouter()






@router.get("/")
async def create_user():

    print('hihihi')
    users = await User.all()
    # for user in users:
    #     for key, value in user.__dict__.items():
    #         print(key, " : ", value)
    #     print()
    user = users[0]
    print(user.access_id)

    return {"User count":len(users)}






@router.post("/test")
async def test(user:User = Depends(AuthRoute.spider_launch)):

    print('im in the route')

    return {'status':'dunno'}



@router.get("/create_user")
async def create_user():


    # await User.create_new_user(
    #     email="no@no.com"
    # )


    return {'bleh':"bahsdfdsa"}