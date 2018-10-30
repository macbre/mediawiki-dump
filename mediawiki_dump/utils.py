"""
Utility functions
"""
from datetime import datetime, timezone


def parse_date_string(date):
    """
    Converts date as string (e.g. "2004-05-25T02:19:28Z") to UNIX timestamp (uses UTC, always)
    :type date str
    :rtype: datetime
    """

    # https://docs.python.org/3.6/library/datetime.html#strftime-strptime-behavior
    # http://strftime.org/
    parsed = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')  # string parse time

    # now apply UTC timezone
    return parsed.replace(tzinfo=timezone.utc)
