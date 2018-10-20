"""
This script take Faroese Wikipedia dump and generates a list of unique words that it contains
"""
import logging

from corpus.dumps import WikipediaDump
from corpus.reader import DumpReaderArticles
from corpus.tokenizer import clean, tokenize

logging.basicConfig(level=logging.INFO)


def words_from_dump(wiki):
    """
    :type wiki str
    """
    logger = logging.getLogger('words_from_dump')

    dump = WikipediaDump(wiki)
    pages = DumpReaderArticles().read(dump)

    long_words = []

    # pages = list(pages)[:50]  # debug, take only first X pages

    for _, _, title, content in pages:
        if str(content).startswith('#REDIRECT'):
            logger.debug('%s is a redirect, skipping...', title)
            continue

        article_words = tokenize(clean(title + ' ' + content))

        # make it lower
        article_words = [str(word).lower() for word in article_words]

        # make it unique and sort it
        article_words = sorted(set(article_words))

        # add long words
        long_words += [word for word in article_words if len(word) > 10]

        # print('---')
        # print(title, content, article_words)

    # sort long words
    long_words = sorted(set(long_words), key=len, reverse=True)

    # show top X
    for i, word in enumerate(long_words[:50]):
        print('%d %s - %d' % (i+1, word, len(word)))


if __name__ == "__main__":
    words_from_dump(wiki='fo')
