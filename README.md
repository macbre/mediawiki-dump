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
