# from ..spider import RequestsSpider
from webscraping.spider_base import AsyncSpider
from asyncio import sleep as async_sleep


class SynchronySpider(AsyncSpider):

    url = "https://www.synchrony.com/for-consumers.html#credit-cards"

    async def run(self):
        # super().__init__()
        # print('Synchrony Spider finished')
        # async_sleep(3)

        yield {'snychrony':'blahh'}

        # await self.close_session()
        # print('synchrony finished')
        # return

# Synchrony()