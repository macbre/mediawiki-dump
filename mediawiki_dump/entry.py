"""
A class representing dump entry
"""
from. utils import parse_date_string


# pylint: disable=too-many-instance-attributes
class DumpEntry:
    """
    An entry in XML dump
    """
    # pylint: disable=too-many-arguments
    def __init__(self, namespace: int, page_id: int, url: str, title: str,
                 content: str, revision_id: int, timestamp: str, contributor: str = None):
        self.namespace = namespace
        self.page_id = page_id
        self.url = url
        self.title = title
        self.content = content
        self.revision_id = revision_id
        self.timestamp = timestamp
        self.contributor = contributor

    @property
    def unix_timestamp(self) -> float:
        """When was given article most recently edited
        """
        return parse_date_string(self.timestamp).timestamp()

    def is_anon(self) -> bool:
        """Was this edit made by an anonymous contributor?
        """
        return self.contributor is None

    def __repr__(self) -> str:
        return '<{} "{}" by {} at {}>'.format(
            self.__class__.__name__,
            self.title,
            self.contributor if not self.is_anon() else 'Anonymous',
            parse_date_string(self.timestamp).isoformat()
        )
