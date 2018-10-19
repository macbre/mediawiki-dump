"""
CLasses that support fetching dumps
"""
import bz2
import logging
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

    def get_url(self):
        """
        :rtype: str
        """
        raise NotImplementedError('fetch method needs to be implemented')

    def fetch(self):
        """
        :rtype: bytes
        """
        url = self.get_url()

        self.logger.info('Fetching %s dump from <%s>...', self.wiki, url)
        res = self.http.get(url)
        self.logger.info('HTTP %s (%d kB fetched)', res.status_code, len(res.content) / 1024)

        return res.content

    def get_content(self):
        """
        :rtype: str
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
        :rtype: str
        """
        return bz2.decompress(self.fetch())


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
        :rtype: str
        """
        raise NotImplementedError('To be implemented')
