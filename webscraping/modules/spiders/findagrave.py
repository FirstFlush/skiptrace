# from ..spider import RequestsSpider, PlaywrightSpider
# from asyncio import sleep as async_sleep
# import time

from webscraping.spider import AsyncSpider, RequestsSpider, PlaywrightSpider

class FindAGraveSpider(AsyncSpider):

    url = "https://www.findagrave.com/memorial/search?linkedToName=john+smith&page=1#sr-9339398"

    async def run(self):
        res = await self.get(self.url)
        if res is None:
            return

        self.cook_soup(markup=res)
        names = self.soup.select('h2.name-grave > i')
        # for name in names:
        #     print(name.get_text())
        # print(len(names))
        yield {'names':names}

    # async def fetch(self, url):
    #     """Simulated asynchronous fetch function."""
    #     await asyncio.sleep(1)  # Simulating async IO-bound operation
    #     # In a real scenario, you'd fetch the content and parse it here
    #     return {"url": url, "data": "Some scraped data from " + url}

    # async def run(self):
    #     """Asynchronous generator yielding data as it scrapes each URL."""
    #     for url in self.urls:
    #         scraped_data = await self.fetch(url)
    #         yield scraped_data


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
