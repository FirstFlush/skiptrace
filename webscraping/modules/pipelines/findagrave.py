from webscraping.pipeline import BasePipeline
from skip.models import SkipRelative

class FindAGravePipeline(BasePipeline):

    tables = [SkipRelative]
    