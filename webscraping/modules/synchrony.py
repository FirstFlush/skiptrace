# from ..spider import RequestsSpider
from webscraping.spider import RequestsSpider




class Synchrony(RequestsSpider):

    url = "https://www.synchrony.com/for-consumers.html#credit-cards"

    def run(self):
        # super().__init__()
        print('Synchrony spider')
        return

# Synchrony()