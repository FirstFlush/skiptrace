import logging
import random
import requests
import time
import ua_generator

from enum import Enum
from bs4 import BeautifulSoup, FeatureNotFound, ParserRejectedMarkup
from playwright.sync_api import sync_playwright
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

import config

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=f"{config.LOG_DIR}/scraping.log",
    level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s'
)

class LogLevel(Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


class WebScrapingError(BaseException):
    """Base class for all webscraping errors."""
    pass

class SpiderError(WebScrapingError):
    """Base class for spider-related errors."""
    pass

class SpiderHttpError(SpiderError):
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
    """Base class for all webscrapers"""
    soup = None
    url = None

    def __init__(self):
        self.ua:str = ua_generator.generate(device="desktop").text

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
            self.log(CookSoupError(repr(e)), LogLevel.ERROR)
        try:
            self._check_soup()
        except CheckSoupError as e:
            self.log(CheckSoupError(repr(e)), LogLevel.ERROR)

        return

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

    def random_delay(self, l:int=3, h:int=8):
        """Random time delay. 
        To make us look more human :)
        """
        time.sleep(random.randint(l, h))
        return


class RequestsSpider(Spider):
    """This class gives python's requests library functionality to
    our spiders.
    """

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


    def get(self, session:requests.Session, **kwargs) -> requests.Response | None:
        """Wrapper function for requests library session.get() to
        include error handling.

        *If the request fails this method will return None. Always check 
        to make sure the return value is a Response object and not None.
        """
        res = None
        try:
            res = session.get(self.url, timeout=2, **kwargs)
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


