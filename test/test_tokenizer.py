from unittest import TestCase

from corpus.tokenizer import Tokenizer


class TestTokenizerClean(TestCase):

    def setUp(self):
        self.tokenizer = Tokenizer()

    def test(self):
        assert self.tokenizer.clean('Foo bar.') == 'Foo bar.'
        assert self.tokenizer.clean('foo bar') == 'foo bar'

        # basic formatting
        assert self.tokenizer.clean("''italic''") == 'italic'
        assert self.tokenizer.clean("'''bold'''") == 'bold'

        # headings
        assert self.tokenizer.clean('==foo==') == 'foo'
        assert self.tokenizer.clean('===Foo===') == 'Foo'
        assert self.tokenizer.clean('=== Foo ===') == 'Foo'
        assert self.tokenizer.clean('== Brot úr søguni hjá Klaksvíkar kommunu ==') \
            == 'Brot úr søguni hjá Klaksvíkar kommunu'

        # links
        assert self.tokenizer.clean('[[foo]] bar') == 'foo bar'
        assert self.tokenizer.clean('[[foo]]s bar') == 'foos bar'
        assert self.tokenizer.clean('av [[Norðoyar|Norðuroyggjum]].') == 'av Norðuroyggjum.'
        assert self.tokenizer.clean('* [[Svínoy]]') == 'Svínoy'
        assert self.tokenizer.clean('[[File:Kommunur í Føroyum]] foo') == 'foo'
        assert self.tokenizer.clean('[[Bólkur:Kommunur í Føroyum]] foo') == 'foo'

        # lists
        assert self.tokenizer.clean('* 123\n*245\n* 346 * 789') == '123\n245\n346 * 789'
        assert self.tokenizer.clean('* 123\n** 245') == '123\n245'

        # external links
        assert self.tokenizer.clean('[http://www.klaksvik.fo Heimasíðan hjá Klaksvíkar kommunu]') \
            == 'Heimasíðan hjá Klaksvíkar kommunu'

        # templates
        assert self.tokenizer.clean('{{Kommunur}}') == ''

    def test_complex(self):
        assert self.tokenizer.clean('=== Á [[Borðoy|Borðoynni]] ===') == 'Á Borðoynni'
        assert self.tokenizer.clean("''' Klaksvíkar kommuna''' er næststørsta kommuna í [[Føroyar|Føroyum]].") \
            == 'Klaksvíkar kommuna er næststørsta kommuna í Føroyum.'

    def test_from_file(self):
        # https://fo.wikipedia.org/wiki/Klaksv%C3%ADkar_kommuna
        with open('test/fixtures/text.txt', 'rt') as f:
            text = f.read().strip()

        with open('test/fixtures/expected.txt', 'rt') as f:
            expected = f.read().strip()

        assert self.tokenizer.clean(text) == expected
