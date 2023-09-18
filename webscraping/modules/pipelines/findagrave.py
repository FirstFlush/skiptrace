from webscraping.pipeline_base import Pipeline
from skip.models import SkipRelative
import logging


logger = logging.getLogger("scraping")

class FindAGravePipeline(Pipeline):

    tables = [SkipRelative]
    

    # def process_item(self, item):
    #     pass


    # def __init__(self):
