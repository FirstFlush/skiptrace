# from ..spider import RequestsSpider, PlaywrightSpider
# from asyncio import sleep as async_sleep
# import time

from webscraping.spider import AsyncSpider, RequestsSpider, PlaywrightSpider


class FindAGrave(AsyncSpider):

    url = "https://www.findagrave.com"

    async def run(self):
        res = await self.get(self.url)
        if res is None:
            return

        # self.cook_soup(markup=res)
        # print(self.soup.prettify())

        # bleh = self.soup.select('.grave-search-bg > h1:nth-child(1)')
        # print(bleh)
        # print('FindAGrave Spider finished')
        await self.close_session()
        return
    



class FindARequestsGrave(RequestsSpider):

    url = "https://www.findagrave.com"

    def run(self):
        # super().__init__()
        res = self.get(self.session())
        if res is None:
            return
        
        self.cook_soup(markup=res.content)
        # print(self.soup.prettify())
        # time.sleep(5)
        # bleh = self.soup.select('.grave-search-bg > h1:nth-child(1)')
        print('requests spider')



class FindAPlaywrightGrave(PlaywrightSpider):

    url = "https://www.findagrave.com"

    def __init__(self):
        super().__init__()
        # self.sync('chromium', headless=False)
        # res = self.goto(self.url)
        # if res is None:
        #     return
        
        # self.cook_soup(markup=self.page.content())
        # print(self.soup.prettify())
        # soup = BeautifulSoup(markup=self.page.content(), features='lxml')
        # bleh = soup.select('.grave-search-bg > h1:nth-child(1)')
        # print(bleh)
        print('playwright spider')

        # self.shutdown()

# FindAGrave()
# FindAPlaywrightGrave()
