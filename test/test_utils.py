from mediawiki_dump.utils import parse_date_string


def test_parse_date_string():
    # new Date(1085451568000).toGMTString()
    # "Tue, 25 May 2004 02:19:28 GMT"
    assert parse_date_string("1970-01-01T00:00:00Z").timestamp() == 0
    assert parse_date_string("2004-05-25T02:19:28Z").timestamp() == 1085451568
    assert parse_date_string("2018-10-29T16:01:01Z").timestamp() == 1540828861
