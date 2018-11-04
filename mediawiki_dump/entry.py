"""
A class representing dump entry
"""
from. utils import parse_date_string


class DumpEntry:
    """
    An entry in XML dump
    """
    # pylint: disable=too-many-arguments
    def __init__(self, namespace, page_id, title, content, revision_id, timestamp, contributor):
        """
        :type namespace int
        :type page_id int
        :type title str
        :type content str
        :type revision_id int
        :type timestamp str
        :type contributor str|None
        """
        self.namespace = namespace
        self.page_id = page_id
        self.title = title
        self.content = content
        self.revision_id = revision_id
        self.timestamp = timestamp
        self.contributor = contributor

    @property
    def unix_timestamp(self):
        """
        :rtype: float
        """
        return parse_date_string(self.timestamp).timestamp()

    def is_anon(self):
        """
        :rtype: bool
        """
        return self.contributor is None

    def __repr__(self):
        """
        :rtype: str
        """
        return '<{} "{}" by {} at {}>'.format(
            self.__class__.__name__,
            self.title,
            self.contributor if not self.is_anon() else 'Anonymous',
            parse_date_string(self.timestamp).isoformat()
        )
