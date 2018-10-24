from corpus.dumps import WikiaDump, WikipediaDump
from corpus.reader import DumpReader


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

    assert len(pages) == 2

    assert pages[0][0] == 8  # ns
    assert pages[0][1] == 121  # page_id
    assert pages[0][2] == 'MediaWiki:Logouttext'  # title
    assert str(pages[0][3]).startswith('Tú hevur nú ritað út.')   # content

    assert pages[1][0] == 0  # ns
    assert pages[1][1] == 2201  # page_id
    assert pages[1][2] == 'Klaksvíkar kommuna'  # title
    assert str(pages[1][3]).startswith('{{Infoboks Kommuna|\nnavn              = Klaksvíkar kommuna|')   # content


def test_wikia():
    dump = WikiaDumpFixture()
    reader = DumpReader()

    pages = list(reader.read(dump))
    print(pages)

    assert len(pages) == 3

    assert pages[0][0] == 14  # ns
    assert pages[0][1] == 1  # page_id
    assert pages[0][2] == 'Kategoria:Browse'  # title
    assert str(pages[0][3]).startswith('The main category for this community')   # content

    assert pages[1][0] == 0  # ns
    assert pages[1][1] == 2  # page_id
    assert pages[1][2] == 'Macbre Wiki'  # title
    assert pages[1][3] == '123\n[[Category:Browse]]'   # content
