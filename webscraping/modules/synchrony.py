# from ..base_scrapers import PageGrabber, RequestsMixin#, PlaywrightMixin
from webscraping.base_scrapers import PageGrabber, RequestsMixin
from bs4 import BeautifulSoup

base_url = "https://www.synchrony.com/for-consumers.html#credit-cards"



class SynchronyScraper(PageGrabber, RequestsMixin):

    url = "https://www.synchrony.com/for-consumers.html#credit-cards"

    def __init__(self):
        super().__init__()
        





SynchronyScraper()