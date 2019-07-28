"""
CLasses that support fetching dumps
"""
import bz2
import logging

from typing import Generator, Iterator

from hashlib import md5
from os.path import isfile
from tempfile import gettempdir

from mwclient import Site
import requests
from requests.exceptions import HTTPError


class DumpError(Exception):
    """
    Generic exception class
    """


class BaseDump:
    """
    A generic dump class

    Wikipedia or Wikia dumps should have a separate class that customizes get_url() method
    """
    ARCHIVE_FORMAT = 'bz2'

    def __init__(self, wiki, full_history=False):
        """
        :type wiki str
        :type full_history bool
        """
        self.wiki = wiki
        self.logger = logging.getLogger(self.__class__.__name__)

        self.http = requests.session()
        self.http.headers['User-Agent'] = \
            'python-mediawiki-dump (+https://github.com/macbre/mediawiki-dump)'

        # do we want a full history or just the latest revisions?
        self.full_history = full_history

    def get_cache_filename(self, url):
        """
        Return a hashed filename of cache entry for a given URL

        :type url str
        :rtype: str
        """
        _hash = md5()
        _hash.update(url.encode('utf-8'))

        return 'mediawiki_dump_{hash}.{extension}'.format(
            hash=_hash.hexdigest(), extension=self.ARCHIVE_FORMAT)

    def get_url(self):
        """
        :rtype: str
        """
        raise NotImplementedError('fetch method needs to be implemented')

    def fetch(self):
        """
        This method should be used internally only. Clients should call get_content().

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
            self.logger.info('HTTP %s (%d kB will be fetched)',
                             response.status_code, int(response.headers['content-length']) / 1024)

            # raise an exception and do not set a cache entry
            try:
                response.raise_for_status()
            except HTTPError as ex:
                self.logger.error('Failed to fetch a dump', exc_info=True)
                raise DumpError('Failed to fetch a dump, request ended with HTTP {}'.
                                format(ex.response.status_code))

            # read the response as a stream and put it into cache file
            # http://docs.python-requests.org/en/master/user/advanced/#body-content-workflow
            #
            # before using a stream reading and parsing of Faroese dump made the words_from_dump.py
            # script took ~460 MB of memory, after the change - ~60 MB
            with open(cache_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

                response.close()
                self.logger.info("Cache set")
        else:
            self.logger.info("Reading from cache")

        # return a stream of compressed data from the cache file
        return open(cache_filename, 'rb')

    def get_content(self) -> Generator[str, None, None]:
        """Yields processed pieces of content
        """
        raise NotImplementedError('fetch method needs to be implemented')


class WikipediaDump(BaseDump):
    """
    Class for fetching Wikipedia dumps from https://dumps.wikimedia.org
    """
    def get_url(self):
        return 'https://dumps.wikimedia.org/{wiki}/latest/' \
               '{wiki}-latest-pages-meta-{version}.xml.bz2'.\
            format(wiki='{}wiki'.format(self.wiki),
                   version='history' if self.full_history else 'current')

    def get_content(self) -> Generator[str, None, None]:
        """Yields processed pieces of content
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
    """
    ARCHIVE_FORMAT = '7z'

    def get_url(self) -> str:
        # https://muppet.wikia.com/wiki/Special:Statistics
        return 'https://s3.amazonaws.com/wikia_xml_dumps/{}/{}/{}_pages_{version}.xml.7z'.format(
            self.wiki[0], self.wiki[:2], self.wiki,
            version='full' if self.full_history else 'current')

    def get_content(self) -> Generator[str, None, None]:
        """Yields processed pieces of content
        """
        # https://github.com/Changaco/python-libarchive-c#usage
        try:
            import libarchive
        except AttributeError:
            # AttributeError: undefined symbol: archive_errno
            raise DumpError("Failed to import libarchive with 7zip support")

        with self.fetch() as handler:
            with libarchive.file_reader(handler.name) as archive:
                for entry in archive:
                    for block in entry.get_blocks():
                        yield block


class LocalFileDump(BaseDump):
    """
    This class can be used to load locally stored XML dump file
    """
    def __init__(self, dump_file: str):
        super(LocalFileDump, self).__init__('')
        self.dump_file = dump_file

    def get_url(self):
        pass

    def get_content(self):
        """Yields processed pieces of content
        """
        return open(self.dump_file, 'rt')


class LocalWikipediaDump(WikipediaDump):
    """
    This class can be used to load locally stored XML, bz2 compressed dump file
    """
    def __init__(self, dump_file: str):
        super(LocalWikipediaDump, self).__init__('')
        self.dump_file = dump_file

    def get_url(self):
        pass

    def fetch(self):
        return open(self.dump_file, 'rb')


class MediaWikiClientDump(BaseDump):
    """
    This class can be used to fetch "live" dumps from articles on any MediaWiki-powered site
    by using mwclient library
    """
    def __init__(self, site: Site, articles: Iterator[str]):
        """You must provide a mwclient.Site instance and a iterator that yields article names
        """
        # https://mwclient.readthedocs.io/en/latest/index.html
        super(MediaWikiClientDump, self).__init__('')

        self.site = site
        self.articles = list(articles)

    def get_url(self) -> str:
        return self.site.host  # e.g. vim.wikia.com

    def get_content(self) -> str:
        return self.fetch()

    def fetch(self) -> str:
        self.logger.info('Fetching %d pages from %s wiki',
                         len(self.articles), self.get_url())

        # https://www.mediawiki.org/wiki/Manual:Parameters_to_Special:Export
        resp = self.site.raw_call(
            script='index',
            data=dict(
                title='Special:Export',
                curonly='1',
                pages='\n'.join(self.articles),
            ),
            http_method='GET'
        )

        return resp
