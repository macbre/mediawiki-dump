from corpus.dumps import WikipediaDump, WikiaDump


def test_dump_get_url():
    assert WikipediaDump(wiki='fo').get_url() == \
        'https://dumps.wikimedia.org/fowikisource/latest/' \
        'fowikisource-latest-pages-meta-current.xml.bz2'

    assert WikiaDump(wiki='plpoznan').get_url() == \
        'https://s3.amazonaws.com/wikia_xml_dumps/p/pl/plpoznan_pages_current.xml.7z'
