# faroese-corpus
[![Build Status](https://travis-ci.org/macbre/faroese-corpus.svg?branch=master)](https://travis-ci.org/macbre/faroese-corpus)

Faroese corpus taken from Wikipedia dumps.

This repository will contain corpus of Faroese language taken from [the content dump](https://dumps.wikimedia.org/fowikisource/latest/) of [Faroese Wikipedia](https://fo.wikipedia.org).

## `pipenv`

This project uses `pipenv`. [How to install `pipenv`](https://pipenv.readthedocs.io/en/latest/install/#pragmatic-installation-of-pipenv).

## Links

* [ FTS - Färöisk textsamling](https://spraakbanken.gu.se/korp/?mode=faroe)
* [Current XML dump](https://dumps.wikimedia.org/fowikisource/latest/fowikisource-latest-pages-meta-current.xml.bz2) (~14 MB)
* [MediaWiki XML dump format](https://www.mediawiki.org/wiki/Help:Export#Export_format)


## Features

### Tokenizer

Allows you to clean up the wikitext:

```python
>>> from corpus.tokenizer import clean
>>> clean('[[Foo|bar]] is a link')
'bar is a link'
```

And then tokenize the text:

```python
>>> from corpus.tokenizer import tokenize
>>> tokenize('11. juni 2007 varð kunngjørt, at Svínoyar kommuna verður løgd saman við Klaksvíkar kommunu eftir komandi bygdaráðsval.')
['juni', 'varð', 'kunngjørt', 'at', 'Svínoyar', 'kommuna', 'verður', 'løgd', 'saman', 'við', 'Klaksvíkar', 'kommunu', 'eftir', 'komandi', 'bygdaráðsval']
```

### Dump reader

Fetch and parse dumps:

```python
from corpus.dumps import WikipediaDump
from corpus.reader import DumpReader
dump = WikipediaDump('fo')
pages = DumpReader().read(dump)
[title for _, _, title, _ in pages][:10]

['Main Page', 'Brúkari:Jon Harald Søby', 'Forsíða', 'Ormurin Langi', 'Regin smiður', 'Fyrimynd:InterLingvLigoj', 'Heimsyvirlýsingin um mannarættindi', 'Bólkur:Kvæði', 'Bólkur:Yrking', 'Kjak:Forsíða']
```

You can read article pages only as well:

```python
import logging; logging.basicConfig(level=logging.INFO)

from corpus.dumps import WikipediaDump
from corpus.reader import DumpReaderArticles
dump = WikipediaDump('fo')
pages = DumpReaderArticles().read(dump)
[title for _, _, title, _ in pages][:25]
```

Will give you:

```
INFO:DumpReaderArticles:Parsing XML dump...
INFO:WikipediaDump:Fetching fo dump from <https://dumps.wikimedia.org/fowiki/latest/fowiki-latest-pages-meta-current.xml.bz2>...
INFO:WikipediaDump:HTTP 200 (14105 kB fetched)
...
['WIKIng', 'Føroyar', 'Borðoy', 'Eysturoy', 'Fugloy', 'Forsíða', 'Løgmenn í Føroyum', 'GNU Free Documentation License', 'GFDL', 'Opið innihald', 'Wikipedia', 'Alfrøði', '2004', '20. juni', 'WikiWiki', 'Wiki', 'Danmark', '21. juni', '22. juni', '23. juni', 'Lívfrøði', '24. juni', '25. juni', '26. juni', '27. juni']
```
