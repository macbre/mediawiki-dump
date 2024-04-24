import bz2
import pytest

from mediawiki_dump.dumps import LocalFileDump, IteratorDump
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


def test_read_compressed_local_file_as_stream():
    def get_content(file_name: str):
        with bz2.open(file_name, mode="r") as fp:
            yield from fp

    dump = IteratorDump(iterator=get_content(file_name="test/fixtures/dump.xml.bz2"))
    reader = DumpReader()

    pages = [entry.title for entry in reader.read(dump)]
    print(pages)

    assert pages == ["MediaWiki:Logouttext", "Klaksvíkar kommuna"]
