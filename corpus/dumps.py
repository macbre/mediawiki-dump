"""
CLasses that support fetching dumps
"""
import bz2
import logging

from hashlib import md5
from os.path import isfile
from tempfile import gettempdir

import requests


class BaseDump:
    """
    A generic dump class. Wikipedia or Wikia dumps
    should have a separate class that customizes get_url() method
    """

    def __init__(self, wiki):
        """
        :type wiki str
        """
        self.wiki = wiki
        self.logger = logging.getLogger(self.__class__.__name__)

        self.http = requests.session()
        self.http.headers['User-Agent'] = \
            'python-corpus (+https://github.com/macbre/faroese-corpus)'

    @staticmethod
    def get_cache_filename(url):
        """
        Return a hashed filename of cache entry for a given URL

        :type url str
        :rtype: str
        """
        _hash = md5()
        _hash.update(url.encode('utf-8'))

        return 'wikicorpus_{hash}.bz2'.format(hash=_hash.hexdigest())

    def get_url(self):
        """
        :rtype: str
        """
        raise NotImplementedError('fetch method needs to be implemented')

    def fetch(self):
        """
        :rtype: _io.TextIOWrapper
        """
        url = self.get_url()

        cache_filename = '{}/{}'.format(gettempdir(), self.get_cache_filename(url))
        self.logger.info("Checking %s cache file...", cache_filename)

        # check cache
        if not isfile(cache_filename):
            # fetch the resource
            self.logger.info('Fetching %s dump from <%s>...', self.wiki, url)
            response = self.http.get(url, stream=True)
            self.logger.info('HTTP %s (%d kB fetched)',
                             response.status_code, len(response.content) / 1024)

            # read the response as a stream and put it into cache file
            # http://docs.python-requests.org/en/master/user/advanced/#body-content-workflow
            #
            # before using a stream reading and parsing of Faroese dump made the words_from_dump.py
            # script took ~460 MB of memory, after the change - ~60 MB
            with response:
                with open(cache_filename, 'wb') as file:
                    for chunk in response.iter_content():
                        file.write(chunk)

                response.close()
                self.logger.info("Cache set")
        else:
            self.logger.info("Reading from cache")

        # return a stream of compressed data from the cache file
        return open(cache_filename, 'rb')

    def get_content(self):
        """
        :rtype: list[str]
        """
        raise NotImplementedError('fetch method needs to be implemented')


class WikipediaDump(BaseDump):
    """
    Class for fetching Wikipedia dumps from https://dumps.wikimedia.org
    """
    def get_url(self):
        return 'https://dumps.wikimedia.org/{wiki}/latest/' \
               '{wiki}-latest-pages-meta-current.xml.bz2'.format(wiki='{}wiki'.format(self.wiki))

    def get_content(self):
        """
        :rtype: list[str]
        """
        # https://docs.python.org/3.6/library/bz2.html#bz2.BZ2Decompressor
        decompressor = bz2.BZ2Decompressor()

        with self.fetch() as content:
            for chunk in content:
                yield decompressor.decompress(chunk)


class WikiaDump(BaseDump):
    """
    Class for fetching Wikia dumps

    https://community.wikia.com/wiki/Help:Database_download

    TODO: add 7zip archive support
    """
    def get_url(self):
        # https://muppet.wikia.com/wiki/Special:Statistics
        return 'https://s3.amazonaws.com/wikia_xml_dumps/{}/{}/{}_pages_current.xml.7z'.format(
            self.wiki[0], self.wiki[:2], self.wiki)

    def get_content(self):
        """
        :rtype: list[str]
        """
        raise NotImplementedError('To be implemented')
