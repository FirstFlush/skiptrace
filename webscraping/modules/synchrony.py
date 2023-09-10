# from ..spider import RequestsSpider
from webscraping.spider import RequestsSpider




class SynchronyA(RequestsSpider):

    url = "https://www.synchrony.com/for-consumers.html#credit-cards"

    def __init__(self):
        super().__init__()
        


SynchronyA()