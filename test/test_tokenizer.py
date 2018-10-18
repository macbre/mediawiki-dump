from unittest import TestCase

from corpus.tokenizer import Tokenizer


class TestTokenizer(TestCase):

    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_clean(self):
        assert self.tokenizer.clean('Foo bar.') == 'Foo bar.'
        assert self.tokenizer.clean('foo bar') == 'foo bar'

        # links
        assert self.tokenizer.clean('[[foo]] bar') == 'foo bar'
        assert self.tokenizer.clean('[[foo]]s bar') == 'foos bar'
        assert self.tokenizer.clean('av [[Norðoyar|Norðuroyggjum]].') == 'av Norðuroyggjum.'
        assert self.tokenizer.clean('* [[Svínoy]]') == 'Svínoy'

        # external links
        assert self.tokenizer.clean('[http://www.klaksvik.fo Heimasíðan hjá Klaksvíkar kommunu]') \
            == 'Heimasíðan hjá Klaksvíkar kommunu'

        # templates
        assert self.tokenizer.clean('{{Kommunur}}') == ''
