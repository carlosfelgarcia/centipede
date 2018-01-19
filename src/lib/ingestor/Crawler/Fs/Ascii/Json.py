import json
from ..Ascii import Ascii

class Json(Ascii):
    """
    Json crawler.
    """

    def _runParser(self):
        """
        Parse the json contents.
        """
        return json.load(open(self.var('filePath')))

    @classmethod
    def test(cls, pathHolder, parentCrawler):
        """
        Test if the path holder contains a json file.
        """
        if not super(Ascii, cls).test(pathHolder, parentCrawler):
            return False

        return pathHolder.ext() in ['json']


# registration
Json.register(
    'json',
    Json
)