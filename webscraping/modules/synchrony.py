# from ..base_scrapers import PageGrabber, RequestsMixin#, PlaywrightMixin
from webscraping.spider import Spider, RequestsMixin


base_url = "https://www.synchrony.com/for-consumers.html#credit-cards"



class SynchronyScraper(Spider, RequestsMixin):

    url = "https://www.synchrony.com/for-consumers.html#credit-cards"

    def __init__(self):
        super().__init__()
        





SynchronyScraper()