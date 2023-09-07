import requests
import logging
import random
import time
import ua_generator
from playwright.sync_api import sync_playwright
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)


class PageGrabber:

    def __init__(self, url:str):
        self.url = url
        self.ua:str = ua_generator.generate(device="desktop").text


    def random_delay(self, l:int=3, h:int=8):
        """Random time delay. 
        To make us look more human :)
        """
        time.sleep(random.randint(l, h))
        return



class RequestsMixin:
    """Mixin class for PageGrabber to add requests functionality."""

    def _headers(self) -> dict:
        """Currently headers is static except for UA. 
        Will put in functionality here to make the other 
        headers more dynamic.
        """
        headers = {
            "User-Agent": self.ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
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
    """Mixin class for PageGrabber to add playwright functionality."""

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




class FindAGrave(PageGrabber, PlaywrightMixin):

    def __init__(self, url:str):
        super().__init__(url=url)
        self.sync('chromium', headless=False)
        res_pw = self.page.goto(self.url)
        print(type(res_pw))
        self.shutdown()


class FindAnotherGrave(PageGrabber, RequestsMixin):

    def __init__(self, url:str):
        super().__init__(url=url)
        s = self.session()
        print(s.headers)

        # res = s.get(self.url)
        # print(type(res))


# FindAGrave(url="https://www.findagrave.com")
FindAnotherGrave(url="https://www.findagrave.com")


