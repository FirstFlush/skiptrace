from webscraping.spider_base import AsyncSpider, RequestsSpider, PlaywrightSpider


class FindAGraveSpider(AsyncSpider):
# class FindABlehSpider(AsyncSpider):

    url = "https://www.findagrave.com/memorial/search?linkedToName=john+smith&page=1#sr-9339398"

    async def run(self):
        res = await self.get(self.url)
        if res is None:
            return

        self.cook_soup(markup=res)
        names = self.soup.select('h2.name-grave > i')

        yield {'names':names}


class FindAPlaywrightGrave(PlaywrightSpider):
# class FindAGraveSpider(PlaywrightSpider):

    url = "https://www.findagrave.com"

    async def run(self):
        await self.start('chromium', headless=False)
        res = await self.goto(self.url)

        if res is None:
            return
        # self.cook_soup(markup=self.page.content())
        # print(self.soup.prettify())
        # soup = BeautifulSoup(markup=self.page.content(), features='lxml')
        # bleh = soup.select('.grave-search-bg > h1:nth-child(1)')
        # print(bleh)
        print('playwright spider')
        yield {'bleh':'playwright'}



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



# FindAGrave()
# FindAPlaywrightGrave()
