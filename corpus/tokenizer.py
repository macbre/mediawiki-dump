"""
Cleans and tokenizes given text
"""
import re


class Tokenizer(object):

    @staticmethod
    def clean(text):
        """
        :type text str
        :rtype str
        """
        # local links
        text = re.sub(r'\[\[([^|\]]+)\]\]', '\\1', text)  # [[a]] -> a
        text = re.sub(r'\[\[[^|]+\|([^\]]+)\]\]', '\\1', text)  # [[a|b]] -> b

        # external links
        text = re.sub(r'\[http[^\s]+ ([^\]]+)\]', '\\1', text)  # [[http://example.com foo]] -> foo

        # lists
        text = re.sub(r'^\*\s?', '', text)

        # templates
        text = re.sub(r'{{[^}]+}}', '', text)

        return text
