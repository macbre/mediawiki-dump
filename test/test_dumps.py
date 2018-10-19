from corpus.dumps import WikipediaDump, WikiaDump


def test_dump_get_url():
    assert WikipediaDump('fo').get_url() == \
        'https://dumps.wikimedia.org/fowiki/latest/fowiki-latest-pages-meta-current.xml.bz2'

    assert WikiaDump('plpoznan').get_url() == \
        'https://s3.amazonaws.com/wikia_xml_dumps/p/pl/plpoznan_pages_current.xml.7z'
