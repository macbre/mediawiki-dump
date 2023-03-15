from contextlib import contextmanager
from typing import ContextManager, AnyStr
from unittest.mock import patch


import pytest
import responses
from mwclient import Site

from mediawiki_dump.dumps import (
    WikipediaDump,
    WikiaDump,
    MediaWikiClientDump,
    StringDump,
    DumpError,
)
from mediawiki_dump.reader import DumpReader


def test_dump_get_url():
    # https://dumps.wikimedia.org/fowiki/latest/
    assert (
        WikipediaDump("fo").get_url()
        == "https://dumps.wikimedia.org/fowiki/latest/fowiki-latest-pages-meta-current.xml.bz2"
    )

    assert (
        WikipediaDump("fo", full_history=False).get_url()
        == "https://dumps.wikimedia.org/fowiki/latest/fowiki-latest-pages-meta-current.xml.bz2"
    )

    assert (
        WikipediaDump("fo", full_history=True).get_url()
        == "https://dumps.wikimedia.org/fowiki/latest/fowiki-latest-pages-meta-history.xml.bz2"
    )

    # https://poznan.wikia.com/wiki/Specjalna:Statystyka
    assert (
        WikiaDump("plpoznan").get_url()
        == "https://s3.amazonaws.com/wikia_xml_dumps/p/pl/plpoznan_pages_current.xml.7z"
    )

    assert (
        WikiaDump("plpoznan", full_history=True).get_url()
        == "https://s3.amazonaws.com/wikia_xml_dumps/p/pl/plpoznan_pages_full.xml.7z"
    )


def test_get_cache_filename():
    dump = WikipediaDump("fo")
    assert (
        dump.get_cache_filename(dump.get_url())
        == "mediawiki_dump_62da4928a0a307185acaaa94f537d090.bz2"
    )

    dump = WikipediaDump("en")
    assert (
        dump.get_cache_filename(dump.get_url())
        == "mediawiki_dump_7160d38a2668dcc15a33ee6e2a685bbd.bz2"
    )

    dump = WikipediaDump("en", full_history=True)
    assert (
        dump.get_cache_filename(dump.get_url())
        == "mediawiki_dump_84ec5ef573e2d2666b97f82874ae5d67.bz2"
    )


def test_mediawiki_client_dump():
    """Integration test for MediaWikiClientDump class"""
    wiki = Site(host="vim.fandom.com", path="/")
    dump = MediaWikiClientDump(
        wiki, articles=map(str, ["Vim scripts", "Vim_documentation"])
    )

    pages = [entry.title for entry in DumpReader().read(dump)]

    print(dump, pages)
    assert pages == ["Vim scripts", "Vim documentation"]


def test_string_dump():
    assert StringDump("foo").get_content() == "foo"
    assert StringDump("foobarbaz").get_content() != "foo"


@contextmanager
def get_dump_with_mocked_http_response(
    body: AnyStr, status: int = 200
) -> ContextManager[WikipediaDump]:
    dump = WikipediaDump(wiki="test")

    with responses.RequestsMock(assert_all_requests_are_fired=True) as mocked_responses:
        mocked_responses.add(
            method=responses.GET,
            url=dump.get_url(),
            body=body,
            status=status,
            headers={"content-length": str(len(body))},
        )

        yield dump


def test_fetch_handles_http_errors():
    # skip file-based caching in BaseDump cache
    # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch
    with patch("mediawiki_dump.dumps.isfile", return_value=False) as mocked_method:
        with get_dump_with_mocked_http_response(body="Error", status=500) as dump:
            with pytest.raises(DumpError) as ex:
                list(dump.get_content())

            assert "Failed to fetch a dump, request ended with HTTP 500" in str(ex)

    assert mocked_method.call_count == 1, "mocked isfile() was called by BaseDump.fetch"


def test_fetch_via_mocked_http():
    # skip file-based caching in BaseDump cache
    # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch
    with patch("mediawiki_dump.dumps.isfile", return_value=False) as mocked_method:
        body = open("test/fixtures/dump.xml.bz2", "rb").read()

        with get_dump_with_mocked_http_response(body=body, status=200) as dump:
            body = "".join(
                map(
                    lambda item: item.decode("utf8"),
                    dump.get_content(),
                )
            )

    assert mocked_method.call_count == 1, "mocked isfile() was called by BaseDump.fetch"

    assert body.startswith("<mediawiki")
    assert body.endswith("</mediawiki>\n")
