import os
import sys
from glob import glob
from collections import OrderedDict

class InvalidResourceError(Exception):
    """Invalid dependency Error."""

class Resource(object):
    """
    Class used to load custom resources to the ingestor.

    The resources can be custom crawlers, tasks, task wrappers (etc). By default
    any resource specified under the 'INGESTOR_RESOURCE_PATH' is
    automatically loaded during the startup.

    The resources are simply python files that should import all the non-default
    modules under the _perform implementation.

    Also, make sure you always query the singleton instance through the "get"
    method.
    """

    __singleton = None
    __resourceEnvName = "INGESTOR_RESOURCE_PATH"

    def __init__(self):
        """
        Create a resource class (@See Resource.get).
        """
        assert self.__singleton is None, "Can only have one instance!"

        self.__loadedPaths = OrderedDict()
        self.__loadResourceEnvPath()

    def load(self, filePath):
        """
        Load a python resource file to the runtime.

        It can used to load custom crawlers, expressions, task wrappers...
        """
        if not os.path.exists(filePath):
            raise InvalidResourceError(
                'Invalid resource "{0}"!'.format(filePath)
            )

        self.__loadToRuntime(filePath, "external")

    def loaded(self, ignoreFromEnvironment=False):
        """
        Return a list of file paths that have been loaded as resource.
        """
        result = []
        for resourceFilePath, resourceSource in self.__loadedPaths.items():
            if not ignoreFromEnvironment or resourceSource != 'environment':
                result.append(resourceFilePath)

        return result

    @classmethod
    def get(cls):
        """
        Return the singleton resource instance.
        """
        if cls.__singleton is None:
            cls.__singleton = Resource()

        return cls.__singleton

    def __loadToRuntime(self, filePath, source):
        """
        Execute a python resource.
        """
        try:
            exec(open(filePath).read(), globals())
        except Exception as err:
            sys.stderr.write('Error on loading dependency: "{0}"\n'.format(
                filePath
            ))
            sys.stderr.flush()

            raise err
        else:
            # removing any previous occurrence of the same file
            # we don't want to show duplicated resources
            if filePath in self.__loadedPaths:
                del self.__loadedPaths[filePath]

            self.__loadedPaths[filePath] = source

    def __loadResourceEnvPath(self):
        """
        Load all the resources under the resource path environment.
        """
        resourcePaths = os.environ.get(self.__resourceEnvName, '').split(":")[::-1]

        # loading any python file under the resources path
        for resourcePath in filter(os.path.exists, resourcePaths):
            for pythonFile in glob(os.path.join(resourcePath, '*.py')):
                self.__loadToRuntime(pythonFile, 'environment')


# loading resources by triggering the singleton
Resource.get()
