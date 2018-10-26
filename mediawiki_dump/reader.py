"""
Class used to parse provided XML dump and emit a stream of articles content

https://gist.github.com/macbre/1543d945f5244c5c68681966f07e2d6c
"""
import logging

from xml import sax


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

        self.pages_batch = []
        self.pages_count = 0

        # parser state, are we inside <page> or <revision> tag?
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

    def reset_state(self):
        """
        Reset page information
        """
        self.in_page = False
        self.in_revision = False
        self.in_contributor = False

        self.current_title = ''
        self.current_namespace = 0
        self.current_page_id = 0
        self.current_revision_id = 0
        self.current_revision_timestamp = 0
        self.current_content = ''

    def startElement(self, name, attrs):
        # print('>', name, attrs)
        # self.logger.info('> startElement %s %s', name, attrs)

        if name == 'page':
            self.in_page = True
        elif name == 'revision':
            self.in_revision = True
        elif name == 'contributor':
            self.in_contributor = True

        self.tag_content = ''

    def endElement(self, name):
        # print('<', name, self.tag_content)
        # self.logger.info('< endElement %s (%s)', name, self.tag_content)

        if name == 'page':
            self.in_page = False

            # add next page information
            self.logger.debug('Page #%d: %s', self.current_page_id, self.current_title)

            self.pages_batch.append((
                self.current_namespace,
                self.current_page_id,
                self.current_title,
                self.current_content,
                self.current_revision_id,
                self.current_revision_timestamp,
            ))

            self.pages_count += 1

            self.reset_state()
            return
        if name == 'revision':
            self.in_revision = False
            return
        if name == 'contributor':
            self.in_contributor = False
            return

        if self.in_contributor:
            pass
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

    def characters(self, content):
        # print('=', content)
        # self.logger.info('= characters %s', content)

        self.tag_content += content

    def get_pages(self):
        """
        Used by DumpReader to yield pages as we parse the XML dump
        """
        for page in self.pages_batch:
            yield page

        self.pages_batch = []

    def get_pages_count(self):
        """
        :rtype: int
        """
        return self.pages_count


class DumpReader:
    """
    This class uses provided BaseDump instance to read and parse MediaWiki's XML dump
    """
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
        :type dump mediawiki_dump.dumps.BaseDump
        :rtype: list
        """
        self.logger.info('Parsing XML dump...')

        # https://docs.python.org/2/library/xml.etree.elementtree.html#parsing-xml

        # https: // docs.python.org / 3.6 / library / xml.sax.html?highlight = sax  # xml.sax.parse
        handler = DumpHandler()

        parser = sax.make_parser()
        parser.setContentHandler(handler)

        for chunk in dump.get_content():
            parser.feed(chunk)

            # yield pages as we go through XML stream
            for page in handler.get_pages():
                (namespace, page_id, title, content, revision_id, revision_timestamp) = page

                if content == '':
                    # https://fo.wikipedia.org/wiki/Kjak:L%C3%ADvfr%C3%B8%C3%B0i
                    self.logger.warning('Page #%d: %s is empty', page_id, title)
                    continue

                if self.filter_by_namespace(namespace):
                    yield namespace, page_id, title, content, revision_id, revision_timestamp

        self.logger.info('Parsing completed, pages found: %d', handler.get_pages_count())


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
