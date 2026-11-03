"""spec_lexicon: the one reader of term entries (design §10.1), identifiers (§9.6) and the term rules v_t4–v_t6."""
import pathlib
import textwrap

import spec_lexicon

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "glossary"


def test_an_entry_gives_its_category_kinds_and_fields():
    t = spec_lexicon.entry("- **initiative** (kind): the delivery of one request's accepted lines. Plural: "
                           "initiatives. Not: epic.", "spec/index.md")
    assert (t.term, t.category, t.kinds, t.plural, t.nots) == ("initiative", "kind", (), "initiatives", ("epic",))
    t = spec_lexicon.entry("- **status** (attribute of initiative): Values: `proposed`, `started`, `done`, "
                           "`abandoned`. Transitions: `proposed` → `started`: `work start`; `started` → `done`: "
                           "complete.", "x")
    assert t.category == "attribute" and t.kinds == ("initiative",)
    assert t.values == ("`proposed`", "`started`", "`done`", "`abandoned`")
    assert t.transitions == (("`proposed`", "`started`", "`work start`"), ("`started`", "`done`", "complete"))


def test_relation_resource_condition_and_event_entries():
    t = spec_lexicon.entry("- **under** (relation work-item → capability-proposal): a work-item delivers.", "x")
    assert (t.category, t.kinds) == ("relation", ("work-item", "capability-proposal"))
    t = spec_lexicon.entry("- **worker slot** (resource, counted by `workers`): held by every worker.", "x")
    assert (t.category, t.resource) == ("resource", "counted by `workers`")
    t = spec_lexicon.entry("- **open** (condition of initiative): Means: its status is not `done`.", "x")
    assert (t.category, t.kinds, t.means) == ("condition", ("initiative",), "its status is not `done`")
    t = spec_lexicon.entry("- **write** (event): Forms: writes, written.", "x")
    assert t.forms == ("writes", "written")
    t = spec_lexicon.entry("- **`work run`** (actor): the supervisor.", "x")
    assert (t.term, t.category) == ("`work run`", "actor")


def test_an_entry_without_a_category_is_read_with_none():
    t = spec_lexicon.entry("- **status**: an initiative's are `proposed` and `done`.", "spec/index.md")
    assert t.term == "status" and t.category == ""
    assert spec_lexicon.entry("not an entry", "x") is None


def test_read_takes_the_glossary_and_every_capabilitys_terms():
    lex = spec_lexicon.read(FIXTURE)
    terms = {(t.term, t.category) for t in lex.terms}
    assert ("initiative", "kind") in terms and ("`work run`", "actor") in terms
    ledger = [t for t in lex.terms if t.term == "ledger"]
    assert ledger and ledger[0].where == "spec/capabilities/work-queue.md"
    status = [t for t in lex.terms if t.term == "status" and t.kinds == ("work-item",)]
    assert "`awaiting-answer`" in status[0].values and status[0].transitions


def test_ident_maps_a_term_to_a_gf_identifier():
    assert spec_lexicon.ident("work-item", "kind") == "k_work_item"
    assert spec_lexicon.ident("`work run`", "actor") == "a_work_run"
    assert spec_lexicon.ident("spec lock", "resource") == "s_spec_lock"


def test_colliding_identifiers_are_numbered_in_sorted_order():
    lex = spec_lexicon.read(FIXTURE)
    ids = lex.ids()
    assert ids[("attribute", "status", ("capability-proposal",))] == "t_status"
    assert ids[("attribute", "status", ("design-decision",))] == "t_status_2"
    assert ids[("value", "`done`", ("initiative", "status"))] != ids[("value", "`done`", ("work-item", "status"))]


def test_the_fixture_glossary_has_no_problems():
    assert spec_lexicon.problems(spec_lexicon.read(FIXTURE)) == []


def _lexicon(glossary):
    return spec_lexicon.Lexicon(
        [spec_lexicon.entry(b, "spec/index.md") for b in textwrap.dedent(glossary).strip().splitlines()])


def test_problems_give_v_t4_v_t5_and_v_t6():
    lex = _lexicon("""
        - **status**: no category.
        - **initiative** (kind): one.
        - **initiative** (kind): twice.
        - **phase** (attribute of initiative): Values: `a`, `b`.
        - **state** (attribute of initiative): Values: `b`, `c`.
        - **colour** (attribute of balloon): Values: `red`.
        - **a session** (actor): clashes with the kind.
        - **session** (kind): a conversation.
        - **print** (event): a core verb of the grammar.
    """)
    codes = sorted((p[0], p[1]) for p in spec_lexicon.problems(lex))
    assert ("v_t4", "colour") in codes and ("v_t4", "status") in codes
    assert ("v_t5", "`b`") in codes
    assert ("v_t6", "initiative") in codes and ("v_t6", "a session") in codes and ("v_t6", "print") in codes


def test_words_are_every_spelling_a_line_may_use():
    words = spec_lexicon.read(FIXTURE).words()
    assert {"`work run`", "initiative", "`drafted`", "spec lock", "under"} <= words
