import aiodns
import aiohttp
import asyncio
import logging
import random
import requests
import ua_generator

from bs4 import FeatureNotFound, ParserRejectedMarkup
from playwright.async_api import async_playwright, Response as ResponsePlaywright
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

from common.enums import LogLevel
from .exceptions import WebScrapingError, CookSoupError, CheckSoupError, SpiderHttpError
from .soup import SpiderSoup

logger = logging.getLogger('scraping')


class Spider:
    """Base class for all webscrapers"""

    session = None
    url = None
    soup = None
    is_error = False
    error = None
    scraped_data:list[dict] = []
    

    def __init__(self, queue:asyncio.Queue, **kwargs):
        self.ua:str = ua_generator.generate(device="desktop").text
        self.headers:dict = self.create_headers()
        self.queue = queue


    def _check_soup(self):
        """A hook for inserting custom validation of the BeautifulSoup 
        object or markup.
        """
        return


    def _soup(self, markup:str|bytes, **kwargs):
        """Instantiates BeautifulSoup object and sets it to self.soup"""
        try:
            self.soup = SpiderSoup(markup=markup, features='lxml', **kwargs)
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
            self.log(CookSoupError(repr(e)), LogLevel.ERROR)
        try:
            self._check_soup()
        except CheckSoupError as e:
            self.log(CheckSoupError(repr(e)), LogLevel.ERROR)
        return


    def create_headers(self) -> dict:
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


    def log(self, e:WebScrapingError, level:LogLevel=LogLevel.ERROR):
        """Logging method to track all issues related to web scraping."""
        match level:
            case LogLevel.CRITICAL:
                logger.critical(f"{repr(e)}")
            case LogLevel.ERROR:
                logger.error(f"{repr(e)}")
            case LogLevel.WARNING:
                logger.warning(f"{repr(e)}")
            case LogLevel.INFO:
                logger.info(f"{repr(e)}")
            case LogLevel.DEBUG:
                logger.debug(f"{repr(e)}")
            case _:
                logger.critical(f"Unexpected log level: {level}. Original error: {repr(e)}")
        return


    def raise_error(self, e:WebScrapingError, as_e:BaseException, level:LogLevel=LogLevel.ERROR):
        """Logs error with self.log() and then sets self.is_error to True and sets self.error
        to the class name of the error "e".
        """
        self.log(e(repr(as_e)), level)
        self.is_error = True
        self.error = e
        return


    async def random_delay(self, l:int=2, h:int=8):
        """Random time delay. 
        To make us look more human :)
        """
        s = random.randint(l, h)
        await asyncio.sleep(s)
        return


class AsyncSpider(Spider):

    def __init__(self, queue, **kwargs):
        super().__init__(queue, **kwargs)
        self.session = aiohttp.ClientSession()


    async def get(self, url:str=None) -> str:
        """Make an async request via aiohttp module."""
        if url is None:
            url = self.url
        try:
            async with self.session.get(url) as response:
                return await response.text()
        except aiohttp.ClientError as e:
            # self.log(SpiderHttpError(repr(e)), LogLevel.ERROR)
            self.raise_error(SpiderHttpError, e, LogLevel.ERROR)
            await self.close_session()

    async def close_session(self):
        if self.session:
            await self.session.close()


class RequestsSpider(Spider):
    """This class gives python's requests library functionality to
    our spiders.
    """

    def get(self, session:requests.Session, **kwargs) -> requests.Response | None:
        """Wrapper function for requests library's session.get() with
        included error handling.

        *If the request fails this method will return None. Always check 
        to make sure the return value is a Response object and not None.
        """
        res = None
        try:
            res = session.get(self.url, timeout=5, **kwargs)
        except (requests.RequestException, requests.Timeout) as e:
            self.log(SpiderHttpError(repr(e)), LogLevel.ERROR)

        return res


    def session(self, **kwargs) -> requests.Session:
        """Initialize the requests.Session object, along with 
        any attributes of our choosing.
        """
        s = requests.Session()
        s.headers = self._headers()
        for key, value in kwargs.items():
            setattr(s, key, value)
        return s


class PlaywrightSpider(Spider):
    """This class adds playwright functionality to our spider class."""
    
    def __init__(self):
        self.p = None
        self.browser = None
        self.page = None


    def sync(self, browser:str='chromium', headless:bool=False):
        """Sync Chromium webdriver and open the browser."""
        self.p = async_playwright().start()
        match browser:
            case 'firefox':
                self.browser = self.p.firefox.launch(headless=headless)
            case 'webkit':  # requires more libraries
                self.browser = self.p.webkit.launch(headless=headless)
            case _:
                self.browser = self.p.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        return


    def goto(self, url, timeout:float=5000, **kwargs) -> ResponsePlaywright|None:
        """Wrapper function for playwright's page.goto() method to
        includes error handling and logging.

        *timeout is in milliseconds.
        *Ensure this method returns a ResponsePlaywright object, and not None!
        """
        res = None
        try:
            res = self.page.goto(url, timeout=timeout, **kwargs)
        except (PlaywrightError, PlaywrightTimeoutError) as e:
            self.log(SpiderHttpError(repr(e)), LogLevel.ERROR)
        return res


    def shutdown(self):
        """Shuts down the web browser"""
        self.p.stop()
        return


