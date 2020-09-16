from unittest import TestCase

from mediawiki_dump.tokenizer import clean, tokenize, tokenize_filter


class TestTokenizerClean(TestCase):
    def test_basic(self):
        assert clean("Foo bar.") == "Foo bar."
        assert clean("foo bar") == "foo bar"

        assert clean("''italic''") == "italic"
        assert clean("'''bold'''") == "bold"

    def test_headings(self):
        assert clean("==foo==") == "foo"
        assert clean("===Foo===") == "Foo"
        assert clean("=== Foo ===") == "Foo"
        assert (
            clean("== Brot úr søguni hjá Klaksvíkar kommunu ==")
            == "Brot úr søguni hjá Klaksvíkar kommunu"
        )

    def test_links(self):
        assert clean("[[foo]] bar") == "foo bar"
        assert clean("[[foo]]s bar") == "foos bar"
        assert clean("av [[Norðoyar|Norðuroyggjum]].") == "av Norðuroyggjum."
        assert clean("* [[Svínoy]]") == "Svínoy"
        assert clean("[[File:Kommunur í Føroyum]] foo") == "foo"
        assert clean("[[Bólkur:Kommunur í Føroyum]] foo") == "foo"
        assert (
            clean("[[bar]] test [[Bólkur:Kommunur í Føroyum]] foo") == "bar test  foo"
        )

    def test_lists(self):
        assert clean("* 123\n*245\n* 346 * 789") == "123\n245\n346 * 789"
        assert clean("* 123\n** 245") == "123\n245"

    def test_external_links(self):
        assert (
            clean("[http://www.klaksvik.fo Heimasíðan hjá Klaksvíkar kommunu]")
            == "Heimasíðan hjá Klaksvíkar kommunu"
        )

    def test_remove_external_links(self):
        assert (
            clean(
                "Facebook - https://www.facebook.com/fridikarlssonjustesen?fb_dtsg_ag="
                "AdziAVqHQ8WsgyLnRRbFgiD48LLV3ZblI2r6ejYM1ymo-g%3AAdxJZEj_FFlDDrUGSnYE"
                "vseo2SqjBZo3wWNKBausddsffQ link"
            )
            == "Facebook -  link"
        )

        assert (
            clean("http://www.klaksvik.fo Heimasíðan hjá Klaksvíkar kommunu")
            == "Heimasíðan hjá Klaksvíkar kommunu"
        )

    def test_templates(self):
        assert clean("{{Kommunur}}") == ""
        assert clean("{{Kommunur}} bar {{test}}") == "bar"
        assert clean("{{Kommunur}}bar{{test}}test") == "bar test"  # space is kept
        assert clean("{{Kommunur|foo|bar}}") == ""
        assert clean("{{Kommunur|{{foo}}}}") == ""
        assert clean("{{Kommunur|{{foo}}|test}}") == ""
        assert (
            clean("{{Kommunur|{{foo}}|test") == "{{Kommunur|{{foo}}|test"
        )  # unbalanced template wikitext
        assert (
            clean(
                "[[Theodor W. Adorno|Adorno]]{{·}}[[Roland Barthes|Barthes]]"
                "{{·}}[[Jean Baudrillard|Baudrillard]]{{·}}[[Georges Bataille|Bataille]]"
            )
            == "Adorno Barthes Baudrillard Bataille"
        )

    def test_parser_hooks(self):
        assert clean("foo<ref>link</ref>") == "foo"
        assert clean("E = mc<sup>2</sup>") == "E = mc"

    def test_html(self):
        assert clean("foo&nbsp;bar") == "foo bar"
        assert clean("foo<br>") == "foo"
        assert clean("foo<br />") == "foo"
        assert clean("foo<br />bar") == "foo bar"

    def test_magic_words(self):
        assert clean("foo__NOWYSIWYG__bar") == "foobar"
        assert clean("foo\n\n__TOC__\nbar") == "foo\n\n\nbar"
        assert clean("foo __ foo __ bar") == "foo __ foo __ bar"

    def test_tables(self):
        assert (
            clean(
                """
foo
{| class="wikitable"
|-
! 
! Útflutningur
! Innflutningur
|-
| 9.
| {{bar}}
| test
|-
|}
bar
""".strip()
            )
            == "foo\n\nbar"
        )

    def test_complex(self):
        assert clean("=== Á [[Borðoy|Borðoynni]] ===") == "Á Borðoynni"

        assert (
            clean(
                "''' Klaksvíkar kommuna''' er næststørsta kommuna í [[Føroyar|Føroyum]]."
            )
            == "Klaksvíkar kommuna er næststørsta kommuna í Føroyum."
        )

        assert (
            clean(
                "'''Fugloy''', sum hevur fingið navn av tí nógva [[Fuglur|fugli]], "
                "ið har búleikast, er tann minsta av [[Norðoyar|Norðoyum]]"
            )
            == "Fugloy, sum hevur fingið navn av tí nógva fugli, ið har búleikast, er tann minsta av Norðoyum"
        )

        assert (
            clean(
                """
foo{{Infobox cyclist
| birth_date    = {{birth date and age|1987|7|5|df=yes}}
| height        = {{convert|1,81|m|ftin|abbr=on}}
| weight        = {{convert|78|kg|lb|abbr=on}}
}}bar
""".strip()
            )
            == "foo bar"
        )

        assert (
            clean(
                """
{{Infobox person
| name = Wes Craven
| image = Wes Craven 2010.jpg
| image_size = 
| caption = Wes Craven í 2010
| birth_name = Wesley Earl Craven
| birth_date = {{birth date|1939|08|02|df=yes}}
| birth_place = Cleveland, [[Ohio]], [[USA]]
| death_date = {{death date and age|2015|08|30|1939|08|02|df=yes}}
| death_place = [[Los Angeles]], [[California]], [[USA]]
| death_cause = Heilakrabbi
| occupation  = Filmsleikstjóri<br />Rithøvundur<br />Framleiðari<br />Sjónleikari
| years_active = 1971–2015
| spouse = {{marriage|Bonnie Broecker|1964|1969|reason=skild}}<br />{{marriage|[[Mimi Craven]]|1984|1987|reason=skild}}<br />{{marriage|Iya Labunka|2004|2015|reason=deyða sín}}
| website = {{URL|http://www.wescraven.com}}
| children = 2, harímillum Jonathan Craven
}}
""".strip()
            )
            == ""
        )

    def test_from_file(self):
        # https://fo.wikipedia.org/wiki/Klaksv%C3%ADkar_kommuna
        with open("test/fixtures/text.txt", "rt") as f:
            text = f.read().strip()

        with open("test/fixtures/expected.txt", "rt") as f:
            expected = f.read().strip()

        assert clean(text) == expected


class TestTokenizer:
    def test_filter(self):
        assert tokenize_filter("") is False

        assert tokenize_filter("foo") is True

        assert tokenize_filter("aa23") is True
        assert tokenize_filter("1aa23") is True
        assert tokenize_filter("123") is False

    def test(self):
        assert tokenize("Foo bar") == ["Foo", "bar"]

        assert tokenize("Foo  bar") == ["Foo", "bar"]

        assert tokenize("Foo bar.") == ["Foo", "bar"]

        assert tokenize("Foo, bar") == ["Foo", "bar"]

        assert tokenize("Foo: bar") == ["Foo", "bar"]

        assert tokenize("Foo (bar)") == ["Foo", "bar"]

        assert tokenize("Foo bar?") == ["Foo", "bar"]

        assert tokenize('- "Foo bar?" - Yes!') == ["Foo", "bar", "Yes"]

        assert tokenize("Foo bar? Foo bar!") == ["Foo", "bar", "Foo", "bar"]

        assert tokenize("Foo bar ?") == ["Foo", "bar"]

        assert tokenize("Foo bar!") == ["Foo", "bar"]

        assert tokenize("Foo-bar") == ["Foo", "bar"]

        assert tokenize("Foo–bar") == ["Foo", "bar"]

        assert tokenize("Foo/bar") == ["Foo", "bar"]

        assert tokenize("Foo|bar") == ["Foo", "bar"]

        assert tokenize("Foo_bar") == ["Foo", "bar"]

        assert tokenize("Foo&bar") == ["Foo", "bar"]

        # <U+00AD>
        assert tokenize("Foo\xADbar") == ["Foo", "bar"]
        assert tokenize("Foo\u00ADbar") == ["Foo", "bar"]

        assert tokenize("Foo - bar") == ["Foo", "bar"]

        assert tokenize("Foo bar 1 and 5") == ["Foo", "bar", "and"]

        assert tokenize("Foo bar 2 + 2 = four") == ["Foo", "bar", "four"]

        assert tokenize("Foo bar. Test 123") == ["Foo", "bar", "Test"]

        assert tokenize("pennsylvania}}pennsylvania{{flagicon") == [
            "pennsylvania",
            "pennsylvania",
            "flagicon",
        ]

        assert tokenize("Klaksvíkar kommuna er næststørsta kommuna í Føroyum.") == [
            "Klaksvíkar",
            "kommuna",
            "er",
            "næststørsta",
            "kommuna",
            "í",
            "Føroyum",
        ]
