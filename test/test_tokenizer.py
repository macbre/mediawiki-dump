from unittest import TestCase

from corpus.tokenizer import clean, tokenize, tokenize_filter


class TestTokenizerClean(TestCase):

    def test(self):
        assert clean('Foo bar.') == 'Foo bar.'
        assert clean('foo bar') == 'foo bar'

        # basic formatting
        assert clean("''italic''") == 'italic'
        assert clean("'''bold'''") == 'bold'

        # headings
        assert clean('==foo==') == 'foo'
        assert clean('===Foo===') == 'Foo'
        assert clean('=== Foo ===') == 'Foo'
        assert clean('== Brot úr søguni hjá Klaksvíkar kommunu ==') \
            == 'Brot úr søguni hjá Klaksvíkar kommunu'

        # links
        assert clean('[[foo]] bar') == 'foo bar'
        assert clean('[[foo]]s bar') == 'foos bar'
        assert clean('av [[Norðoyar|Norðuroyggjum]].') == 'av Norðuroyggjum.'
        assert clean('* [[Svínoy]]') == 'Svínoy'
        assert clean('[[File:Kommunur í Føroyum]] foo') == 'foo'
        assert clean('[[Bólkur:Kommunur í Føroyum]] foo') == 'foo'

        # lists
        assert clean('* 123\n*245\n* 346 * 789') == '123\n245\n346 * 789'
        assert clean('* 123\n** 245') == '123\n245'

        # external links
        assert clean('[http://www.klaksvik.fo Heimasíðan hjá Klaksvíkar kommunu]') \
            == 'Heimasíðan hjá Klaksvíkar kommunu'

        # templates
        assert clean('{{Kommunur}}') == ''

    def test_complex(self):
        assert clean('=== Á [[Borðoy|Borðoynni]] ===') == 'Á Borðoynni'
        assert clean("''' Klaksvíkar kommuna''' er næststørsta kommuna í [[Føroyar|Føroyum]].") \
            == 'Klaksvíkar kommuna er næststørsta kommuna í Føroyum.'

    def test_from_file(self):
        # https://fo.wikipedia.org/wiki/Klaksv%C3%ADkar_kommuna
        with open('test/fixtures/text.txt', 'rt') as f:
            text = f.read().strip()

        with open('test/fixtures/expected.txt', 'rt') as f:
            expected = f.read().strip()

        assert clean(text) == expected


class TestTokenizer:
    def test_filter(self):
        assert tokenize_filter('') is False

        assert tokenize_filter('foo') is True

        assert tokenize_filter('aa23') is True
        assert tokenize_filter('1aa23') is True
        assert tokenize_filter('123') is False

    def test(self):
        assert tokenize('Foo bar') \
            == ['Foo', 'bar']

        assert tokenize('Foo bar.') \
            == ['Foo', 'bar']

        assert tokenize('Foo, bar') \
            == ['Foo', 'bar']

        assert tokenize('Foo (bar)') \
            == ['Foo', 'bar']

        assert tokenize('Foo bar?') \
            == ['Foo', 'bar']

        assert tokenize('Foo bar ?') \
            == ['Foo', 'bar']

        assert tokenize('Foo bar!') \
            == ['Foo', 'bar']

        assert tokenize('Foo-bar') \
            == ['Foo', 'bar']

        assert tokenize('Foo - bar') \
            == ['Foo', 'bar']

        assert tokenize('Foo bar 1 and 5') \
            == ['Foo', 'bar', 'and']

        assert tokenize('Foo bar 1 * 5') \
            == ['Foo', 'bar']

        assert tokenize('Foo bar. Test 123') \
            == ['Foo', 'bar', 'Test']

        assert tokenize('Klaksvíkar kommuna er næststørsta kommuna í Føroyum.') \
            == ['Klaksvíkar', 'kommuna', 'er', 'næststørsta', 'kommuna', 'í', 'Føroyum']
