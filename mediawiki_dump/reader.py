"""
Class used to parse provided XML dump and emit a stream of articles content

https://gist.github.com/macbre/1543d945f5244c5c68681966f07e2d6c
"""
import logging
from typing import Generator

from xml import sax
from xml.sax.xmlreader import AttributesImpl

from .dumps import BaseDump
from .entry import DumpEntry


class DumpHandler(sax.ContentHandler):
    """
    SAX ContentHandler instance of Wikipedia context XML dumps

      <page>
        <title>Wikipedia:All pages by title</title>
        <ns>4</ns>
        <id>4</id>
        <restrictions>sysop</restrictions>
        <revision>
          <id>6498</id>
          <timestamp>2004-05-25T02:19:28Z</timestamp>
          <contributor>
            <ip>82.68.206.22</ip>
          </contributor>
          <model>wikitext</model>
          <format>text/x-wiki</format>
          <text xml:space="preserve">foo bar</text>
          <sha1>edilrfbz8rbsr9mvl8dflarkw56ojy5</sha1>
        </revision>
      </page>
    """

    # https://www.mediawiki.org/wiki/Help:Export#Export_format
    # https://docs.python.org/3.6/library/xml.sax.handler.html#xml.sax.handler.ContentHandler

    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super(DumpHandler, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

        self.entries_batch = []
        self.entries_count = 0

        # attributes from <mediawiki> root XML tag
        self.metadata = None

        # nodes from <siteinfo> XML tag
        self.siteinfo = dict()
        self.base_url = None

        # parser state, are we inside <page> or <revision> tag?
        self.in_siteinfo = False
        self.in_page = False
        self.in_revision = False
        self.in_contributor = False

        # concatenated content of tags
        self.tag_content = ''

        # currently parsed page dump
        self.current_title = ''
        self.current_namespace = 0
        self.current_page_id = 0
        self.current_revision_id = 0
        self.current_revision_timestamp = 0
        self.current_content = ''
        self.current_contributor = None

    def reset_state(self):
        """
        Reset page information
        """
        self.in_siteinfo = False
        self.in_page = False
        self.in_revision = False
        self.in_contributor = False

        self.current_title = ''
        self.current_namespace = 0
        self.current_page_id = 0
        self.current_revision_id = 0
        self.current_revision_timestamp = 0
        self.current_content = ''
        self.current_contributor = None

    def startElement(self, name: str, attrs: AttributesImpl):
        """
        Run when a parser enters new element
        """
        # print('>', name, attrs)
        # self.logger.info('> startElement %s %s', name, attrs)

        if name == 'siteinfo':
            self.in_siteinfo = True
        elif name == 'page':
            self.in_page = True
        elif name == 'revision':
            self.in_revision = True
        elif name == 'contributor':
            self.in_contributor = True
        elif name == 'mediawiki':
            self.metadata = dict(zip(attrs.keys(), attrs.values()))

        self.tag_content = ''

    # pylint: disable=too-many-branches
    def endElement(self, name: str):
        # print('<', name, self.tag_content)
        # self.logger.info('< endElement %s (%s)', name, self.tag_content)

        if name == 'siteinfo':
            self.in_siteinfo = False
            self.reset_state()
            return
        if name == 'page':
            self.in_page = False
            self.reset_state()
            return
        if name == 'revision':
            self.in_revision = False

            # add next entry information
            self.logger.debug('Page #%d: %s', self.current_page_id, self.current_title)

            # build entry URL
            url = self.get_base_url() + self.current_title.replace(' ', '_')

            self.entries_batch.append((
                self.current_namespace,
                self.current_page_id,
                url,
                self.current_title,
                self.current_content,
                self.current_revision_id,
                self.current_revision_timestamp,
                self.current_contributor,
            ))

            self.entries_count += 1
            return
        if name == 'contributor':
            self.in_contributor = False
            return

        if self.in_contributor:
            if name == 'username':
                self.current_contributor = self.tag_content
        elif self.in_revision:
            if name == 'id':
                self.current_revision_id = int(self.tag_content)
            elif name == 'timestamp':
                self.current_revision_timestamp = self.tag_content
            elif name == 'text':
                self.current_content = self.tag_content
        elif self.in_page:
            if name == 'title':
                self.current_title = self.tag_content
            elif name == 'ns':
                self.current_namespace = int(self.tag_content)
            elif name == 'id':
                self.current_page_id = int(self.tag_content)
        elif self.in_siteinfo:
            if name in ['dbname', 'base', 'generator']:
                self.siteinfo[name] = self.tag_content

    def characters(self, content: str):
        # print('=', content)
        # self.logger.info('= characters %s', content)

        self.tag_content += content

    def get_entries(self) -> Generator[tuple, None, None]:
        """
        Used by DumpReader to yield pages as we parse the XML dump
        """
        for entry in self.entries_batch:
            yield entry

        self.entries_batch = []

    def get_entries_count(self) -> int:
        """
        :rtype: int
        """
        return self.entries_count

    def get_metadata(self) -> dict:
        """
        :rtype: dict|None
        """
        return self.metadata

    def get_siteinfo(self) -> dict:
        """
        :rtype: dict
        """
        return self.siteinfo

    def get_base_url(self) -> str:
        """
        :rtype: str
        """
        # e.g. base URL <https://pl.wikipedia.org/wiki/Wikipedia:Strona_g%C5%82%C3%B3wna>
        # will return <https://pl.wikipedia.org/wiki/>
        if self.base_url is None:
            main_page = str(self.siteinfo.get('base'))
            self.base_url = '/'.join(main_page.split('/')[0:-1])
            self.base_url += '/'  # ends with slash

        return self.base_url


class DumpReader:
    """
    This class uses provided BaseDump instance to read and parse MediaWiki's XML dump
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        # https://docs.python.org/2/library/xml.etree.elementtree.html#parsing-xml
        self.handler = DumpHandler()

    @staticmethod
    def filter_by_namespace(namespace: int) -> bool:
        """
        :type namespace int
        :rtype bool
        """
        return isinstance(namespace, int)

    def read(self, dump: BaseDump) -> Generator[DumpEntry, None, None]:
        """Read a dump and emit DumpEntry objects
        """
        self.logger.info('Parsing XML dump...')

        parser = sax.make_parser()
        parser.setContentHandler(self.handler)

        for chunk in dump.get_content():
            parser.feed(chunk)

            # yield pages as we go through XML stream
            for page in self.handler.get_entries():
                (namespace, page_id, url, title,
                 content, revision_id, revision_timestamp, contributor) = page

                if self.filter_by_namespace(namespace):

                    if content == '':
                        # https://fo.wikipedia.org/wiki/Kjak:L%C3%ADvfr%C3%B8%C3%B0i
                        self.logger.warning('Page #%d: %s is empty', page_id, title)
                        continue

                    yield DumpEntry(
                        namespace, page_id, url, title, content,
                        revision_id, revision_timestamp, contributor
                    )

        self.logger.info('Parsing completed, entries found: %d', self.handler.get_entries_count())

    def get_dump_language(self) -> str:
        """
        :rtype: str
        """
        return self.handler.get_metadata().get('xml:lang')

    def get_base_url(self) -> str:
        """
        :rtype: str
        """
        return self.handler.get_base_url()


class DumpReaderArticles(DumpReader):
    """
    Use this class to get article pages only
    """
    @staticmethod
    def filter_by_namespace(namespace: int) -> bool:
        """Process NS_MAIN articles only
        """
        return namespace == 0
