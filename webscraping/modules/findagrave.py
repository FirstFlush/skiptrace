# from ..spider import RequestsSpider, PlaywrightSpider

from webscraping.spider import RequestsSpider, PlaywrightSpider


class FindAGrave(RequestsSpider):

    url = "https://www.findagrave.com"

    def __init__(self):
        super().__init__()
        res = self.get(self.session())
        if res is None:
            return
        
        self.cook_soup(markup=res.content)
        print(self.soup.prettify())

        bleh = self.soup.select('.grave-search-bg > h1:nth-child(1)')
        print(bleh)


class FindAPlaywrightGrave(PlaywrightSpider):

    url = "https://www.findagrave.com"

    def __init__(self):
        super().__init__()
        self.sync('chromium', headless=False)
        res = self.goto(self.url)
        if res is None:
            return
        
        self.cook_soup(markup=self.page.content())
        print(self.soup.prettify())
        # soup = BeautifulSoup(markup=self.page.content(), features='lxml')
        # bleh = soup.select('.grave-search-bg > h1:nth-child(1)')
        # print(bleh)

        self.shutdown()

FindAGrave()
# FindAPlaywrightGrave()
