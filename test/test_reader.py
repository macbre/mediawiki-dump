from mediawiki_dump.dumps import WikiaDump, WikipediaDump
from mediawiki_dump.entry import DumpEntry
from mediawiki_dump.reader import DumpReader, DumpReaderArticles


class WikipediaDumpFixture(WikipediaDump):
    def __init__(self):
        super(WikipediaDumpFixture, self).__init__('')

    def get_url(self):
        pass

    def fetch(self):
        return open('test/fixtures/dump.xml.bz2', 'rb')


class WikiaDumpFixture(WikiaDump):
    def __init__(self):
        super(WikiaDumpFixture, self).__init__('')

    def get_url(self):
        pass

    def fetch(self):
        return open('test/fixtures/dump.xml.7z', 'rb')


class PlainDumpFixture(WikiaDump):
    def __init__(self):
        super(PlainDumpFixture, self).__init__('')

    def get_url(self):
        pass

    def get_content(self):
        return open('test/fixtures/dump.xml', 'rt')


def test_wikipedia():
    dump = WikipediaDumpFixture()
    reader = DumpReader()

    pages = list(reader.read(dump))

    assert len(pages) == 2, "Dump has two items"
    assert isinstance(pages[0], DumpEntry)

    entry = pages[0]
    assert entry.namespace == 8  # ns
    assert entry.page_id == 121  # page_id
    assert entry.title == 'MediaWiki:Logouttext'  # title
    assert str(entry.content).startswith('Tú hevur nú ritað út.')   # content
    assert entry.revision_id == 18683  # revision ID
    assert entry.unix_timestamp == 1146089189  # revision UNIX timestamp
    assert entry.contributor == 'Quackor'  # author

    entry = pages[1]
    assert entry.namespace == 0  # ns
    assert entry.page_id == 2201  # page_id
    assert entry.title == 'Klaksvíkar kommuna'  # title
    assert str(entry.content).startswith('{{Infoboks Kommuna|\nnavn              = Klaksvíkar kommuna|')   # content
    assert entry.revision_id == 341301  # revision ID
    assert entry.unix_timestamp == 1478696410  # revision UNIX timestamp
    assert entry.contributor == 'EileenSanda'  # author


def test_wikia():
    dump = WikiaDumpFixture()
    reader = DumpReader()

    pages = list(reader.read(dump))
    print(pages)

    assert len(pages) == 3, "Dump has three items"

    assert pages[0].namespace == 14  # ns
    assert pages[0].page_id == 1  # page_id
    assert pages[0].title == 'Kategoria:Browse'  # title
    assert str(pages[0].content).startswith('The main category for this community')   # content
    assert pages[0].revision_id == 1  # revision ID
    assert pages[0].unix_timestamp == 1476301866  # revision UNIX timestamp
    assert pages[0].contributor == 'Default'  # author

    assert pages[1].namespace == 0  # ns
    assert pages[1].page_id == 2  # page_id
    assert pages[1].title == 'Macbre Wiki'  # title
    assert pages[1].content == '123\n[[Category:Browse]]'   # content
    assert pages[1].revision_id == 338  # revision ID
    assert pages[1].unix_timestamp == 1520427072  # revision UNIX timestamp
    assert pages[1].contributor == 'Macbre'  # author


def test_wikia_content_pages():
    dump = WikiaDumpFixture()
    reader = DumpReaderArticles()

    pages = list(reader.read(dump))
    print(pages)

    assert len(pages) == 1, "There is only one content pages in the dump"


def test_plain_dump():
    dump = PlainDumpFixture()
    reader = DumpReaderArticles()

    pages = list(reader.read(dump))
    print(pages)

    assert len(pages) == 3, "There are three entries in the dump, but only two pages"

    assert pages[0].title == 'Page title'  # title
    assert pages[0].unix_timestamp == 979564500  # revision UNIX timestamp
    assert pages[0].contributor == 'Foobar'  # author

    assert pages[1].title == 'Page title'  # title
    assert pages[1].unix_timestamp == 979564227  # revision UNIX timestamp
    assert pages[1].contributor == 'Foobar'  # author
    assert pages[1].is_anon() is False

    assert pages[2].title == 'Talk:Page title'  # title
    assert pages[2].unix_timestamp == 979567380  # revision UNIX timestamp
    assert pages[2].contributor is None  # an anonymous contributor
    assert pages[2].is_anon() is True
