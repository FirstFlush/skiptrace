import logging
import random
import requests
import time
import ua_generator
from playwright.sync_api import sync_playwright
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

from bs4 import BeautifulSoup, FeatureNotFound, ParserRejectedMarkup

logging.basicConfig(level=logging.WARNING)


class SpiderError(BaseException):
    """Base class for spider-related errors."""
    pass


class HttpResponseError(SpiderError):
    """Raised when HTTP request returns a status code of
    4xx or 5xx.
    """
    pass

class CookSoupError(SpiderError):
    """Raised when scraper's self.soup() method fails."""
    pass

class CheckSoupError(SpiderError):
    """Raised when the scraper's _check_soup() method fails."""
    pass

class MajorSoupParsingError(Exception):
    """Raised when BeautifulSoup fails to find the selection
    in the markdown and must therefore report a corrupt entry.
    """
    pass

class MinorSoupParsingError(Exception):
    """Raised when BeautifulSoup fails to find the selection
    in the markdown and can simply continue.
    """
    pass


class Spider:

    def __init__(self):
        self.ua:str = ua_generator.generate(device="desktop").text
        self.soup = None


    def _check_soup(self):
        """A hook for inserting custom validation of the BeautifulSoup 
        object or markup.
        """
        return


    def _soup(self, markup:str|bytes, **kwargs):
        """Instantiates BeautifulSoup object and sets it to self.soup"""
        try:
            self.soup = BeautifulSoup(markup=markup, features='lxml', **kwargs)
        except (FeatureNotFound, ValueError, ParserRejectedMarkup) as e:
            raise e
        return


    def cook_soup(self, markup:str|bytes, **kwargs):
        """Wrapper method for instantiating the BeautifulSoup object
        with error handling
        """
        try:
            self._soup(markup, **kwargs)
        except (FeatureNotFound, ValueError, ParserRejectedMarkup) as e:
            raise CookSoupError(f"An error occurred: {e}") from e
        try:
            self._check_soup()
        except CheckSoupError as e:
            raise CheckSoupError(f"An error occurred: {e}") from e

        return


    def random_delay(self, l:int=3, h:int=8):
        """Random time delay. 
        To make us look more human :)
        """
        time.sleep(random.randint(l, h))
        return


class RequestsMixin:
    """Mixin class for Spider to add requests functionality."""

    def _headers(self) -> dict:
        """Currently headers is static except for UA. 
        Will put in functionality here to make the other 
        headers more dynamic.
        """
        headers = {
            "User-Agent": self.ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "DNT": "1",  # Do Not Track Request Header
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1",   
        }
        return headers


    def session(self, **kwargs) -> requests.Session:
        """Initialize the requests.Session object, along with 
        any attributes of our choosing.
        """
        s = requests.Session()
        s.headers = self._headers()
        for key, value in kwargs.items():
            setattr(s, key, value)
        return s


class PlaywrightMixin:
    """Mixin class for Spider to add playwright functionality."""

    def sync(self, browser:str='chromium', headless:bool=False):
        """Sync Chromium webdriver and open the browser."""
        self.p = sync_playwright().start()
        match browser:
            case 'firefox':
                self.browser = self.p.firefox.launch(headless=headless)
            case 'webkit':  # requires more libraries
                self.browser = self.p.webkit.launch(headless=headless)
            case _:
                self.browser = self.p.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        return


    def shutdown(self):
        """Shuts down the web browser"""
        self.p.stop()
        return
    
    # def sync(self, headless:bool=False):
    #     """Sync Chromium webdriver and navigate to the base URL."""
    #     with sync_playwright() as p:
    #         self.browser = p.chromium.launch(headless=headless)
    #         self.page = self.browser.new_page()
    #         res = self.page.goto(self.url)
    #     return




# class FindAGrave(Spider, PlaywrightMixin):

#     def __init__(self):
#         # super().__init__()
#         self.sync('chromium', headless=False)
#         res_pw = self.page.goto(self.url)
#         soup = BeautifulSoup(markup=self.page.content(), features='lxml')
#         bleh = soup.select('.grave-search-bg > h1:nth-child(1)')
#         print(bleh)



#         self.shutdown()


# class FindAnotherGrave(Spider, RequestsMixin):

#     def __init__(self):
#         s = self.session()
        
#         res = s.get(self.url)
#         soup = BeautifulSoup(markup=res.content, features='lxml')
#         bleh = soup.select('.grave-search-bg > h1:nth-child(1)')
#         print(bleh)

        # res = s.get(self.url)
        # print(type(res))


# FindAGrave(url="https://www.findagrave.com")
# FindAnotherGrave(url="https://www.findagrave.com")

