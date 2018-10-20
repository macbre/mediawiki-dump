"""
Cleans and tokenizes given text
"""
import re


def clean(text):
    """
    :type text str
    :rtype: str
    """
    # basic formatting
    text = re.sub(r"'''?([^']+)'''?", '\\1', text)

    # headings
    text = re.sub(r'^=+\s?([^=]+)\s?=+', lambda matches: matches.group(1).strip(),
                  text, flags=re.MULTILINE)  # == a == -> a

    # files and other links with namespaces
    text = re.sub(r'\[\[[^:\]]+:[^\]]+\]\]', '', text)  # [[foo:b]] -> ''

    # local links
    text = re.sub(r'\[\[([^|\]]+)\]\]', '\\1', text)  # [[a]] -> a
    text = re.sub(r'\[\[[^|]+\|([^\]]+)\]\]', '\\1', text)  # [[a|b]] -> b

    # external links
    text = re.sub(r'\[http[^\s]+ ([^\]]+)\]', '\\1', text)  # [[http://example.com foo]] -> foo

    # lists
    text = re.sub(r'^\*+\s?', '', text, flags=re.MULTILINE)

    # templates
    text = re.sub(r'{{[^}]+}}', '', text)  # {{foo}}

    # tables
    text = re.sub(r'{\|[^}]+\|}', '', text)  # {|foo..|}

    # parser hooks
    text = re.sub(r'<[^>]+>[^<]+</[^>]+>', '', text)  # <ref>foo</ref>

    # HTML
    text = re.sub(r'<[^>]+/?>', '', text)  # <br> / <br />
    text = text.replace('&nbsp;', ' ')

    return text.strip()


def tokenize_filter(text):
    """
    :type text str
    :rtype: bool
    """
    if text == '':
        return False

    if text[0].isdigit() and re.fullmatch(r'\d+', text):
        return False

    if text in ['*']:
        return False

    return True


def tokenize(text, filter_func=tokenize_filter):
    """
    :type text str
    :type filter_func callable
    :rtype: list[str]
    """
    # clean up the text
    text = re.sub(r'[?.,:;!()"]', '', text)  # remove noise

    text = text.strip()

    # tokenize
    parts = re.split(r'[-\s]', text)

    parts = filter(filter_func, parts)

    return list(parts)
