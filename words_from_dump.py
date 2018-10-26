"""
This script take Faroese Wikipedia dump and generates a list of unique words that it contains
"""
import sys
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
    logger.info('Processing dump of "%s" wiki...', wiki)

    dump = WikipediaDump(wiki)
    pages = DumpReaderArticles().read(dump)

    long_words = []

    # pages = list(pages)[:50]  # debug, take only first X pages

    for _, _, title, content, *_ in pages:
        if str(content).startswith('#REDIRECT'):
            logger.debug('%s is a redirect, skipping...', title)
            continue

        article_words = tokenize(clean(title + ' ' + content))

        # make it lower
        article_words = [str(word).lower() for word in article_words]

        # make it unique and sort it
        article_words = sorted(set(article_words))

        # add long words (and filter out words with X)
        words_from_article = [word for word in article_words if len(word) > 10 and 'x' not in word]

        if 'filmsleikstjóririthøvundurframleiðarisjónleikari' in words_from_article:
            logger.info('Word found in %s', title)
            print(content)

        long_words += words_from_article

        # print('---')
        # print(title, content, article_words)

    # sort long words
    long_words = sorted(set(long_words), key=len, reverse=True)

    # show top X
    for i, word in enumerate(long_words[:50]):
        print('%d %s - %d' % (i+1, word, len(word)))


if __name__ == "__main__":
    words_from_dump(wiki=sys.argv[1] if len(sys.argv) > 1 else 'fo')
