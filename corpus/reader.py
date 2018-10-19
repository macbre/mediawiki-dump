"""
Class used to parse provided XML dump and emit a stream of articles content

https://gist.github.com/macbre/1543d945f5244c5c68681966f07e2d6c
"""
import logging

from xml.etree import ElementTree


class DumpReader:
    """
    This class uses provided BaseDump instance to read and parse MediaWiki's XML dump

    https://www.mediawiki.org/wiki/Help:Export#Export_format
    https://docs.python.org/2/library/xml.etree.elementtree.html#parsing-xml
    """
    NAMESPACES = {
        'dump': 'http://www.mediawiki.org/xml/export-0.10/'
    }

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def filter_by_namespace(namespace):
        """
        :type namespace int
        :rtype bool
        """
        return isinstance(namespace, int)

    def read(self, dump):
        """
        :type dump corpus.dumps.BaseDump
        :rtype list[str]
        """
        self.logger.info('Parsing XML dump...')

        root = ElementTree.fromstring(dump.get_content())

        for page in root.findall('dump:page', self.NAMESPACES):
            title = page.find('dump:title', self.NAMESPACES).text
            namespace = int(page.find('dump:ns', self.NAMESPACES).text)
            page_id = int(page.find('dump:id', self.NAMESPACES).text)

            revision = page.find('dump:revision', self.NAMESPACES)
            content = revision.find('dump:text', self.NAMESPACES).text

            self.logger.info('Page #%d: %s', page_id, title)

            if self.filter_by_namespace(namespace):
                yield namespace, page_id, title, content


class DumpReaderArticles(DumpReader):
    """
    Use this class to get article pages only
    """
    @staticmethod
    def filter_by_namespace(namespace):
        """
        :type namespace int
        :rtype bool
        """
        return namespace == 0
