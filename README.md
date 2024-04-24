# mediawiki-dump
[![PyPI](https://img.shields.io/pypi/v/mediawiki_dump.svg)](https://pypi.python.org/pypi/mediawiki_dump)
[![Downloads](https://pepy.tech/badge/mediawiki_dump)](https://pepy.tech/project/mediawiki_dump)
[![CI](https://github.com/macbre/mediawiki-dump/actions/workflows/tests.yml/badge.svg)](https://github.com/macbre/mediawiki-dump/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/macbre/mediawiki-dump/badge.svg?branch=master)](https://coveralls.io/github/macbre/mediawiki-dump?branch=master)

```
pip install mediawiki_dump
```

[Python3 package](https://pypi.org/project/mediawiki_dump/) for working with [MediaWiki XML content dumps](https://www.mediawiki.org/wiki/Manual:Backing_up_a_wiki#Backup_the_content_of_the_wiki_(XML_dump)).

[Wikipedia](https://dumps.wikimedia.org/) (bz2 compressed) and [Wikia](https://community.fandom.com/wiki/Help:Database_download) (7zip) content dumps are supported.

## Dependencies

In order to read 7zip archives (used by Wikia's XML dumps) you need to install [`libarchive`](http://libarchive.org/):

```
sudo apt install libarchive-dev
```

## API

### Tokenizer

Allows you to clean up the wikitext:

```python
from mediawiki_dump.tokenizer import clean
clean('[[Foo|bar]] is a link')
'bar is a link'
```

And then tokenize the text:

```python
from mediawiki_dump.tokenizer import tokenize
tokenize('11. juni 2007 varð kunngjørt, at Svínoyar kommuna verður løgd saman við Klaksvíkar kommunu eftir komandi bygdaráðsval.')
['juni', 'varð', 'kunngjørt', 'at', 'Svínoyar', 'kommuna', 'verður', 'løgd', 'saman', 'við', 'Klaksvíkar', 'kommunu', 'eftir', 'komandi', 'bygdaráðsval']
```

### Dump reader

Fetch and parse dumps (using a local file cache):

```python
from mediawiki_dump.dumps import WikipediaDump
from mediawiki_dump.reader import DumpReader

dump = WikipediaDump('fo')
pages = DumpReader().read(dump)

[page.title for page in pages][:10]

['Main Page', 'Brúkari:Jon Harald Søby', 'Forsíða', 'Ormurin Langi', 'Regin smiður', 'Fyrimynd:InterLingvLigoj', 'Heimsyvirlýsingin um mannarættindi', 'Bólkur:Kvæði', 'Bólkur:Yrking', 'Kjak:Forsíða']
```

`read` method yields the `DumpEntry` object for each revision.

By using `DumpReaderArticles` class you can read article pages only:

```python
import logging; logging.basicConfig(level=logging.INFO)

from mediawiki_dump.dumps import WikipediaDump
from mediawiki_dump.reader import DumpReaderArticles

dump = WikipediaDump('fo')
reader = DumpReaderArticles()
pages = reader.read(dump)

print([page.title for page in pages][:25])

print(reader.get_dump_language())  # fo
```

Will give you:

```
INFO:DumpReaderArticles:Parsing XML dump...
INFO:WikipediaDump:Checking /tmp/wikicorpus_62da4928a0a307185acaaa94f537d090.bz2 cache file...
INFO:WikipediaDump:Fetching fo dump from <https://dumps.wikimedia.org/fowiki/latest/fowiki-latest-pages-meta-current.xml.bz2>...
INFO:WikipediaDump:HTTP 200 (14105 kB will be fetched)
INFO:WikipediaDump:Cache set
...
['WIKIng', 'Føroyar', 'Borðoy', 'Eysturoy', 'Fugloy', 'Forsíða', 'Løgmenn í Føroyum', 'GNU Free Documentation License', 'GFDL', 'Opið innihald', 'Wikipedia', 'Alfrøði', '2004', '20. juni', 'WikiWiki', 'Wiki', 'Danmark', '21. juni', '22. juni', '23. juni', 'Lívfrøði', '24. juni', '25. juni', '26. juni', '27. juni']
```

## Reading Wikia's dumps

 ```python
import logging; logging.basicConfig(level=logging.INFO)

from mediawiki_dump.dumps import WikiaDump
from mediawiki_dump.reader import DumpReaderArticles

dump = WikiaDump('plnordycka')
pages = DumpReaderArticles().read(dump)

print([page.title for page in pages][:25])
```

Will give you:

```
INFO:DumpReaderArticles:Parsing XML dump...
INFO:WikiaDump:Checking /tmp/wikicorpus_f7dd3b75c5965ee10ae5fe4643fb806b.7z cache file...
INFO:WikiaDump:Fetching plnordycka dump from <https://s3.amazonaws.com/wikia_xml_dumps/p/pl/plnordycka_pages_current.xml.7z>...
INFO:WikiaDump:HTTP 200 (129 kB will be fetched)
INFO:WikiaDump:Cache set
INFO:WikiaDump:Reading wikicorpus_f7dd3b75c5965ee10ae5fe4643fb806b file from dump
...
INFO:DumpReaderArticles:Parsing completed, entries found: 615
['Nordycka Wiki', 'Strona główna', '1968', '1948', 'Ormurin Langi', 'Mykines', 'Trollsjön', 'Wyspy Owcze', 'Nólsoy', 'Sandoy', 'Vágar', 'Mørk', 'Eysturoy', 'Rakfisk', 'Hákarl', '1298', 'Sztokfisz', '1978', '1920', 'Najbardziej na północ', 'Svalbard', 'Hamferð', 'Rok w Skandynawii', 'Islandia', 'Rissajaure']
```

## Fetching full history

Pass `full_history` to `BaseDump` constructor to fetch the XML content dump with full history:

```python
import logging; logging.basicConfig(level=logging.INFO)

from mediawiki_dump.dumps import WikiaDump
from mediawiki_dump.reader import DumpReaderArticles

dump = WikiaDump('macbre', full_history=True)  # fetch full history, including old revisions
pages = DumpReaderArticles().read(dump)

print('\n'.join([repr(page) for page in pages]))
```

Will give you:

```
INFO:DumpReaderArticles:Parsing completed, entries found: 384
<DumpEntry "Macbre Wiki" by Default at 2016-10-12T19:51:06+00:00>
<DumpEntry "Macbre Wiki" by Wikia at 2016-10-12T19:51:05+00:00>
<DumpEntry "Macbre Wiki" by Macbre at 2016-11-04T10:33:20+00:00>
<DumpEntry "Macbre Wiki" by FandomBot at 2016-11-04T10:37:17+00:00>
<DumpEntry "Macbre Wiki" by FandomBot at 2017-01-25T14:47:37+00:00>
<DumpEntry "Macbre Wiki" by Ryba777 at 2017-04-10T11:20:25+00:00>
<DumpEntry "Macbre Wiki" by Ryba777 at 2017-04-10T11:21:20+00:00>
<DumpEntry "Macbre Wiki" by Macbre at 2018-03-07T12:51:12+00:00>
<DumpEntry "Main Page" by Wikia at 2016-10-12T19:51:05+00:00>
<DumpEntry "FooBar" by Anonymous at 2016-11-08T10:15:33+00:00>
<DumpEntry "FooBar" by Anonymous at 2016-11-08T10:15:49+00:00>
...
<DumpEntry "YouTube tag" by FANDOMbot at 2018-06-05T11:45:44+00:00>
<DumpEntry "Maps" by Macbre at 2018-06-06T08:51:24+00:00>
<DumpEntry "Maps" by Macbre at 2018-06-07T08:17:13+00:00>
<DumpEntry "Maps" by Macbre at 2018-06-07T08:17:36+00:00>
<DumpEntry "Scary transclusion" by Macbre at 2018-07-24T14:52:20+00:00>
<DumpEntry "Lua" by Macbre at 2018-09-11T14:04:15+00:00>
<DumpEntry "Lua" by Macbre at 2018-09-11T14:14:24+00:00>
<DumpEntry "Lua" by Macbre at 2018-09-11T14:14:37+00:00>
```

## Reading dumps of selected articles

You can use [`mwclient` Python library](https://mwclient.readthedocs.io/en/latest/index.html)
and fetch "live" dumps of selected articles from any MediaWiki-powered site.

```python
import mwclient
site = mwclient.Site('vim.fandom.com', path='/')

from mediawiki_dump.dumps import MediaWikiClientDump
from mediawiki_dump.reader import DumpReaderArticles

dump = MediaWikiClientDump(site, ['Vim documentation', 'Tutorial'])

pages = DumpReaderArticles().read(dump)

print('\n'.join([repr(page) for page in pages]))
```

Will give you:

```
<DumpEntry "Vim documentation" by Anonymous at 2019-07-05T09:39:47+00:00>
<DumpEntry "Tutorial" by Anonymous at 2019-07-05T09:41:19+00:00>
```

## Finding pages with a specific [parser tag](https://www.mediawiki.org/wiki/Manual:Tag_extensions)

Let's find pages where no longer supported `<place>` tag is still used:

```python
import logging; logging.basicConfig(level=logging.INFO)

from mediawiki_dump.dumps import WikiaDump
from mediawiki_dump.reader import DumpReader

dump = WikiaDump('plpoznan')
pages = DumpReader().read(dump)

with_places_tag = [
    page.title
    for page in pages
    if '<place ' in page.content
]

logging.info('Pages found: %d', len(with_places_tag))

with open("pages.txt", mode="wt", encoding="utf-8") as fp:
    for entry in with_places_tag:
        fp.write(entry + "\n")

logging.info("pages.txt file created")
```

## Reading dumps from local files

You can also read dumps from local, non-compressed XML files:

```python
from mediawiki_dump.dumps import LocalFileDump
from mediawiki_dump.reader import DumpReader

dump = LocalFileDump(dump_file="test/fixtures/dump.xml")
reader = DumpReader()

pages = [entry.title for entry in reader.read(dump)]
print(dump, pages)
```

## Reading dumps from compressed local files

Or any other iterators (like HTTP responses):

```python
import bz2

from mediawiki_dump.dumps import IteratorDump
from mediawiki_dump.reader import DumpReader

def get_content(file_name: str):
    with bz2.open(file_name, mode="r") as fp:
        yield from fp

dump = IteratorDump(iterator=get_content(file_name="test/fixtures/dump.xml.bz2"))
reader = DumpReader()

pages = [entry.title for entry in reader.read(dump)]
print(dump, pages)
```
