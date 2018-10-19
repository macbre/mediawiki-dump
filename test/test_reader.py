from corpus.dumps import BaseDump
from corpus.reader import DumpReader


class DumpFixture(BaseDump):
    def __init__(self):
        super(DumpFixture, self).__init__('')

    def get_url(self):
        pass

    def get_content(self):
        with open('test/fixtures/dump.xml', 'rt') as f:
            return f.read()


def test_with_fixture():
    dump = DumpFixture()
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
