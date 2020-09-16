from mediawiki_dump.entry import DumpEntry


def test_dump_entry_repr():
    entry = DumpEntry(
        namespace=0,
        page_id=0,
        url="http://example.com",
        title="FooBar",
        content="",
        revision_id=123,
        timestamp="2018-10-29T16:01:01Z",
        contributor="Editor",
    )

    assert repr(entry) == '<DumpEntry "FooBar" by Editor at 2018-10-29T16:01:01+00:00>'
    assert entry.is_anon() is False


def test_dump_entry_is_anon():
    entry = DumpEntry(
        namespace=0,
        page_id=0,
        url="http://example.com",
        title="FooBar",
        content="",
        revision_id=123,
        timestamp="2018-10-31T16:01:01Z",
        contributor=None,
    )

    assert (
        repr(entry) == '<DumpEntry "FooBar" by Anonymous at 2018-10-31T16:01:01+00:00>'
    )
    assert entry.is_anon() is True
