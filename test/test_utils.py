from mediawiki_dump.utils import datetime_to_timestamp


def test_datetime_to_timestamp():
    # new Date(1085451568000).toGMTString()
    # "Tue, 25 May 2004 02:19:28 GMT"
    assert datetime_to_timestamp('1970-01-01T00:00:00Z') == 0
    assert datetime_to_timestamp('2004-05-25T02:19:28Z') == 1085451568
    assert datetime_to_timestamp('2018-10-29T16:01:01Z') == 1540828861
