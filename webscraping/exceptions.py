
class WebScrapingError(BaseException):
    """Base class for all webscraping errors."""
    pass

class SpiderError(WebScrapingError):
    """Base class for spider-related errors."""
    pass

class SpiderLaunchError(WebScrapingError):
    """Base class for errors related to the spider launcher."""
    def __init__(self, broken_spiders:int):
        self.message = f"{broken_spiders} broken spiders." 


class SpiderModuleNotFound(SpiderLaunchError):
    """Spider module can not be imported. Please check the file path and class name."""
    pass

class BrokenSpidersError(SpiderLaunchError):
    """Raised when 1 or more spiders raises an error and fails to scrape."""
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