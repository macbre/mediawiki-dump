from mediawiki_dump.dumps import WikiaDump, WikipediaDump
from mediawiki_dump.reader import DumpReader


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


def test_wikipedia():
    dump = WikipediaDumpFixture()
    reader = DumpReader()

    pages = list(reader.read(dump))

    assert len(pages) == 2, "Dump has two items"
    assert len(pages[0]) == 6, "Each item has six members"

    assert pages[0][0] == 8  # ns
    assert pages[0][1] == 121  # page_id
    assert pages[0][2] == 'MediaWiki:Logouttext'  # title
    assert str(pages[0][3]).startswith('Tú hevur nú ritað út.')   # content
    assert pages[0][4] == 18683  # revision ID
    assert pages[0][5] == '2006-04-26T22:06:29Z'  # revision timestamp

    assert pages[1][0] == 0  # ns
    assert pages[1][1] == 2201  # page_id
    assert pages[1][2] == 'Klaksvíkar kommuna'  # title
    assert str(pages[1][3]).startswith('{{Infoboks Kommuna|\nnavn              = Klaksvíkar kommuna|')   # content
    assert pages[1][4] == 341301  # revision ID
    assert pages[1][5] == '2016-11-09T13:00:10Z'  # revision timestamp


def test_wikia():
    dump = WikiaDumpFixture()
    reader = DumpReader()

    pages = list(reader.read(dump))
    print(pages)

    assert len(pages) == 3, "Dump has three items"
    assert len(pages[0]) == 6, "Each item has six members"

    assert pages[0][0] == 14  # ns
    assert pages[0][1] == 1  # page_id
    assert pages[0][2] == 'Kategoria:Browse'  # title
    assert str(pages[0][3]).startswith('The main category for this community')   # content
    assert pages[0][4] == 1  # revision ID
    assert pages[0][5] == '2016-10-12T19:51:06Z'  # revision timestamp

    assert pages[1][0] == 0  # ns
    assert pages[1][1] == 2  # page_id
    assert pages[1][2] == 'Macbre Wiki'  # title
    assert pages[1][3] == '123\n[[Category:Browse]]'   # content
    assert pages[1][4] == 338  # revision ID
    assert pages[1][5] == '2018-03-07T12:51:12Z'  # revision timestamp
