import os
import unittest
from ....BaseTestCase import BaseTestCase
from ingestor.Crawler.Fs import Path
from ingestor.PathHolder import PathHolder
from ingestor.Crawler.Fs.Image import Png

class PngTest(BaseTestCase):
    """Test Exr crawler."""

    __pngFile = os.path.join(BaseTestCase.dataDirectory(), "test.png")

    def testPngCrawler(self):
        """
        Test that the Png crawler test works properly.
        """
        crawler = Path.create(PathHolder(self.__pngFile))
        self.assertIsInstance(crawler, Png)

    def testPngVariables(self):
        """
        Test that variables are set properly.
        """
        crawler = Path.create(PathHolder(self.__pngFile))
        self.assertEqual(crawler.var("type"), "png")
        self.assertEqual(crawler.var("category"), "image")
        self.assertEqual(crawler.var("imageType"), "single")
        # Current version of Oiio doesn't work with png.
        # Skipping this test for now.
        # self.assertEqual(crawler.var("width"), 640)
        # self.assertEqual(crawler.var("height"), 480)


if __name__ == "__main__":
    unittest.main()
