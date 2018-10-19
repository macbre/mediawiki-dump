from corpus.dumps import WikipediaDump, WikiaDump


def test_dump_get_url():
    assert WikipediaDump('fo').get_url() == \
        'https://dumps.wikimedia.org/fowiki/latest/fowiki-latest-pages-meta-current.xml.bz2'

    assert WikiaDump('plpoznan').get_url() == \
        'https://s3.amazonaws.com/wikia_xml_dumps/p/pl/plpoznan_pages_current.xml.7z'


def test_get_cache_filename():
    dump = WikipediaDump('fo')
    assert dump.get_cache_filename(dump.get_url()) == 'wikicorpus_62da4928a0a307185acaaa94f537d090.bz2'

    dump = WikipediaDump('en')
    assert dump.get_cache_filename(dump.get_url()) == 'wikicorpus_7160d38a2668dcc15a33ee6e2a685bbd.bz2'
