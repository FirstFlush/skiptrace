# Class for bringing BeautifulSoup parsing functionality 
# to our spiders.

from bs4 import BeautifulSoup


class SpiderParser(BeautifulSoup):

    def __init__(self, markup, features, **kwargs):
        super().__init__(markup=markup, features=features, **kwargs)
    