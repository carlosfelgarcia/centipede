import os
import glob
import unittest
from ...BaseTestCase import BaseTestCase
from ingestor.Crawler.Fs import Path
from ingestor.PathHolder import PathHolder
from ingestor.Crawler.Fs.Render import ExrRender
from ingestor.Crawler.Crawler import InvalidVarError
from ingestor.Crawler.Crawler import InvalidTagError

class PathTest(BaseTestCase):
    """Test Directory crawler."""

    __dir = os.path.join(BaseTestCase.dataDirectory(), "glob")
    __turntableFile = os.path.join(__dir, "images", "RND_ass_lookdev_default_beauty_tt.1001.exr")

    def testPathCrawler(self):
        """
        Test that the Path crawler test is not implemented.
        """
        pathHolder = PathHolder(self.__dir)
        self.assertRaises(NotImplementedError, Path.test, pathHolder, None)

    def testPathGlob(self):
        """
        Test the glob functionality.
        """
        crawler = Path.create(PathHolder(self.__dir))
        crawlers = crawler.glob()
        result = glob.glob("{}/**".format(self.__dir), recursive=True)
        result = list(map(lambda x: x.rstrip("/"), result))
        crawlerPaths = list(map(lambda x: x.var("filePath"), crawlers))
        self.assertCountEqual(result, crawlerPaths)

        crawlers = crawler.glob(filterTypes=["turntable"])
        crawlerPaths = list(map(lambda x: x.var("filePath"), crawlers))
        self.assertEqual(crawlerPaths, [self.__turntableFile])

        crawlers = crawler.glob(filterTypes=[ExrRender])
        crawlerPaths = list(map(lambda x: x.var("filePath"), crawlers))
        result = glob.glob("{}/**/RND**.exr".format(self.__dir), recursive=True)
        result = list(map(lambda x: x.rstrip("/"), result))
        self.assertCountEqual(result, crawlerPaths)

        crawler = Path.create(PathHolder(self.__turntableFile))
        otherCrawlers = crawler.globFromParent(filterTypes=[ExrRender])
        crawlerPaths = list(map(lambda x: x.var("filePath"), crawlers))
        otherCrawlerPaths = list(map(lambda x: x.var("filePath"), otherCrawlers))
        self.assertCountEqual(crawlerPaths, otherCrawlerPaths)

    def testPathVariables(self):
        """
        Test that the Path Crawler variables are set properly.
        """
        crawler = Path.create(PathHolder(self.__turntableFile))
        name, ext = os.path.splitext(self.__turntableFile)
        self.assertEqual(crawler.var('filePath'), self.__turntableFile)
        self.assertEqual(crawler.var('ext'), ext.lstrip("."))
        self.assertEqual(crawler.var('baseName'), os.path.basename(self.__turntableFile))
        self.assertEqual(crawler.var('name'), os.path.basename(name).split(".")[0])
        self.assertEqual(crawler.var('sourceDirectory'), os.path.dirname(name))
        self.assertRaises(InvalidVarError, crawler.var, "dummyVar")

    def testPathTags(self):
        """
        Test that the Path Crawler tags are set properly.
        """
        crawler = Path.create(PathHolder(self.__turntableFile))
        self.assertRaises(InvalidTagError, crawler.tag, "dummyTag")

    def testCrawlerRegistration(self):
        """
        Test that you can register a new Path crawler.
        """
        class DummyCrawler(Path):
            @classmethod
            def test(cls, pathHolder, parentCrawler):
                return False

        Path.register("dummy", DummyCrawler)
        self.assertIn("dummy", Path.registeredNames())

    def testPathClone(self):
        """
        Test that cloning crawlers works.
        """
        crawler = Path.create(PathHolder(self.__turntableFile))
        clone = crawler.clone()
        self.assertCountEqual(crawler.varNames(), clone.varNames())
        self.assertCountEqual(crawler.contextVarNames(), clone.contextVarNames())
        self.assertCountEqual(crawler.tagNames(), clone.tagNames())
        self.assertRaises(NotImplementedError, super(Path, crawler).clone)


if __name__ == "__main__":
    unittest.main()
