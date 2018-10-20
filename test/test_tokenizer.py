from unittest import TestCase

from corpus.tokenizer import clean, tokenize, tokenize_filter


class TestTokenizerClean(TestCase):

    def test_basic(self):
        assert clean('Foo bar.') == 'Foo bar.'
        assert clean('foo bar') == 'foo bar'

        assert clean("''italic''") == 'italic'
        assert clean("'''bold'''") == 'bold'

    def test_headings(self):
        assert clean('==foo==') == 'foo'
        assert clean('===Foo===') == 'Foo'
        assert clean('=== Foo ===') == 'Foo'
        assert clean('== Brot úr søguni hjá Klaksvíkar kommunu ==') \
            == 'Brot úr søguni hjá Klaksvíkar kommunu'

    def test_links(self):
        assert clean('[[foo]] bar') == 'foo bar'
        assert clean('[[foo]]s bar') == 'foos bar'
        assert clean('av [[Norðoyar|Norðuroyggjum]].') == 'av Norðuroyggjum.'
        assert clean('* [[Svínoy]]') == 'Svínoy'
        assert clean('[[File:Kommunur í Føroyum]] foo') == 'foo'
        assert clean('[[Bólkur:Kommunur í Føroyum]] foo') == 'foo'
        assert clean('[[bar]] test [[Bólkur:Kommunur í Føroyum]] foo') == 'bar test  foo'

    def test_lists(self):
        assert clean('* 123\n*245\n* 346 * 789') == '123\n245\n346 * 789'
        assert clean('* 123\n** 245') == '123\n245'

    def test_external_links(self):
        assert clean('[http://www.klaksvik.fo Heimasíðan hjá Klaksvíkar kommunu]') \
            == 'Heimasíðan hjá Klaksvíkar kommunu'

    def test_templates(self):
        assert clean('{{Kommunur}}') == ''
        assert clean('{{Kommunur}} bar {{test}}') == 'bar'
        assert clean('{{Kommunur|foo|bar}}') == ''
        assert clean('{{Kommunur|{{foo}}|test}}') == ''

    def test_parser_hooks(self):
        assert clean('foo<ref>link</ref>') == 'foo'
        assert clean('E = mc<sup>2</sup>') == 'E = mc'

    def test_html(self):
        assert clean('foo&nbsp;bar') == 'foo bar'
        assert clean('foo<br>') == 'foo'
        assert clean('foo<br />') == 'foo'

    def test_complex(self):
        assert clean('=== Á [[Borðoy|Borðoynni]] ===') == 'Á Borðoynni'

        assert clean("''' Klaksvíkar kommuna''' er næststørsta kommuna í [[Føroyar|Føroyum]].") \
            == 'Klaksvíkar kommuna er næststørsta kommuna í Føroyum.'

        assert clean("'''Fugloy''', sum hevur fingið navn av tí nógva [[Fuglur|fugli]], "
                     "ið har búleikast, er tann minsta av [[Norðoyar|Norðoyum]]") \
            == 'Fugloy, sum hevur fingið navn av tí nógva fugli, ið har búleikast, er tann minsta av Norðoyum'

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

        assert tokenize('Foo: bar') \
            == ['Foo', 'bar']

        assert tokenize('Foo (bar)') \
            == ['Foo', 'bar']

        assert tokenize('Foo bar?') \
            == ['Foo', 'bar']

        assert tokenize('- "Foo bar?" - Yes!') \
            == ['Foo', 'bar', 'Yes']

        assert tokenize('Foo bar? Foo bar!') \
            == ['Foo', 'bar', 'Foo', 'bar']

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
