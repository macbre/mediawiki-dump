"""
Cleans and tokenizes given text
"""
import re


def clean(text):
    """
    :type text str
    :rtype str
    """
    # basic formatting
    text = re.sub(r"'''?([^']+)'''?", '\\1', text)

    # headings
    text = re.sub(r'^=+\s?([^=]+)\s?=+', lambda matches: matches.group(1).strip(),
                  text, flags=re.MULTILINE)  # == a == -> a

    # files and other links with namespaces
    text = re.sub(r'\[\[[^:]+:[^\]]+\]\]', '', text)  # [[foo:b]] -> ''

    # local links
    text = re.sub(r'\[\[([^|\]]+)\]\]', '\\1', text)  # [[a]] -> a
    text = re.sub(r'\[\[[^|]+\|([^\]]+)\]\]', '\\1', text)  # [[a|b]] -> b

    # external links
    text = re.sub(r'\[http[^\s]+ ([^\]]+)\]', '\\1', text)  # [[http://example.com foo]] -> foo

    # lists
    text = re.sub(r'^\*+\s?', '', text, flags=re.MULTILINE)

    # templates
    text = re.sub(r'{{[^}]+}}', '', text)

    return text.strip()


def tokenize(text):
    """
    :type text str
    :rtype list[str]
    """
    raise NotImplementedError()
