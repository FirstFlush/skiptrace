# from ..base_scrapers import PageGrabber, RequestsMixin, PlaywrightMixin

from webscraping.base_scrapers import PageGrabber, RequestsMixin, PlaywrightMixin
from bs4 import BeautifulSoup



class FindAGrave(PageGrabber, RequestsMixin):

    url = "https://www.findagrave.com"

    def __init__(self):
        super().__init__()
        s = self.session()
        res = s.get(self.url)
        self.cook_soup(markup=res.content)
        print(self.soup.prettify())

        # bleh = soup.select('.grave-search-bg > h1:nth-child(1)')
        # print(bleh)



# class FindAPlaywrightGrave(PageGrabber, PlaywrightMixin):

#     url = "https://www.findagrave.com"

#     def __init__(self):
#         super().__init__()
#         self.sync('chromium', headless=False)
#         res_pw = self.page.goto(self.url)
#         soup = self.soup(markup=self.page.content())
#         print(soup.prettify())
#         # soup = BeautifulSoup(markup=self.page.content(), features='lxml')
#         # bleh = soup.select('.grave-search-bg > h1:nth-child(1)')
#         # print(bleh)

        # self.shutdown()

FindAGrave()
# FindAPlaywrightGrave()
