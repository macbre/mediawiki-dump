"""
Cleans and tokenizes given text
"""
import re
from typing import Callable, List


def clean(text: str) -> str:
    """Cleans up the provided wikitext.
    Removes templates, tables, parser hooks, magic words, HTML tags and file embeds.
    Keeps links.
    """
    # basic formatting
    text = re.sub(r"'''?([^']+)'''?", '\\1', text)

    # templates
    # {{foo}}
    # {{foo|{{test}}|123}}
    while '{{' in text:
        start = text.find('{{')
        level = 1
        pos = start + 2

        while pos < len(text):
            # print('>' + text[pos:pos+2] + '<')

            if text[pos:pos+2] == '{{':
                # nested template - enter next level
                level += 1
                pos += 1
            elif text[pos:pos+2] == '}}':
                # nested template - leave this level
                pos += 1
                level -= 1

            # template is now completed
            if level == 0:
                # print(text, start, pos, text[start:pos+1])
                text = text[:start] + ' ' + text[pos+1:]
                break

            # check next character
            pos += 1

        # the template is not well balanced, leave the endless loop
        if level != 0:
            break

    # tables
    text = re.sub(r'{\|[^}]+\|}', '', text)  # {|foo..|}

    # headings
    text = re.sub(r'^=+\s?([^=]+)\s?=+', lambda matches: matches.group(1).strip(),
                  text, flags=re.MULTILINE)  # == a == -> a

    # files and other links with namespaces
    text = re.sub(r'\[\[[^:\]]+:[^\]]+\]\]', '', text)  # [[foo:b]] -> ''

    # local links
    text = re.sub(r'\[\[([^|\]]+)\]\]', '\\1', text)  # [[a]] -> a
    text = re.sub(r'\[\[[^|]+\|([^\]]+)\]\]', '\\1', text)  # [[a|b]] -> b

    text = text.replace('[[', '').replace(']]', '')

    # external links
    text = re.sub(r'\[http[^\s]+ ([^\]]+)\]', '\\1', text)  # [[http://example.com foo]] -> foo
    text = re.sub(r'https?://[^\s]+', '', text)  # remove http://example.com

    # lists
    text = re.sub(r'^\*+\s?', '', text, flags=re.MULTILINE)

    # parser hooks
    text = re.sub(r'<[^>]+>[^<]+</[^>]+>', ' ', text)  # <ref>foo</ref>

    # HTML
    text = re.sub(r'<[^>]+/?>', ' ', text)  # <br> / <br />
    text = text.replace('&nbsp;', ' ')

    # magic words
    text = re.sub(r'__\w+__', '', text)  # __TOC__

    return text.strip()


def tokenize_filter(text: str) -> bool:
    """Used by tokenize function below. Ignores numbers when tokenizing cleaned up wikitext.
    """
    if text == '':
        return False

    if text[0].isdigit() and re.fullmatch(r'\d+', text):
        return False

    return True


def tokenize(text: str, filter_func: Callable = tokenize_filter) -> List[str]:
    """Tokenizes a given text. Usually you want to first pass it via clean() function.
    """
    # clean up the text
    text = re.sub(r'[?.,:;!()=+"]', ' ', text)  # remove noise

    text = text.strip()

    # tokenize
    parts = re.split(r'[-–\s/|_&{}\xAD]', text)

    parts = filter(filter_func, parts)

    return list(parts)
