import pytest
from mediawiki_dump.dumps import LocalFileDump
from mediawiki_dump.reader import DumpReader


def test_read_local_file():
    dump = LocalFileDump(dump_file="test/fixtures/dump.xml")
    reader = DumpReader()

    pages = [entry.title for entry in reader.read(dump)]
    print(dump, pages)

    # "Page title" has two non-empty revision
    assert pages == ["Page title", "Page title", "Talk:Page title"]

    assert reader.get_dump_language() == "en"
    assert reader.get_base_url() == "https://pl.wikipedia.org/wiki/"
    assert reader.handler.get_siteinfo().get("dbname", None) == "plwiki"
