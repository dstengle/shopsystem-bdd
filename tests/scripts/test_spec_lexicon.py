"""spec_lexicon: the one reader of term entries (design §10.1), identifiers (§9.6) and the term rules v_t4–v_t6."""
import pathlib
import textwrap

import spec_lexicon

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "glossary"


def test_an_entry_gives_its_category_kinds_and_fields():
    t = spec_lexicon.entry("- **initiative** (noun): the delivery of one request's accepted lines. Plural: "
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
    t = spec_lexicon.entry("- **worker slot** (noun, counted by `workers`): held by every worker.", "x")
    assert (t.category, t.resource) == ("resource", "counted by `workers`")
    t = spec_lexicon.entry("- **open** (adjective of initiative): the initiative's status is not `done`.", "x")
    assert (t.category, t.kinds, spec_lexicon.gloss(t.text)) == ("condition", ("initiative",),
                                                                 "the initiative's status is not `done`.")
    t = spec_lexicon.entry("- **write** (verb): Forms: writes, written.", "x")
    assert t.forms == ("writes", "written")
    t = spec_lexicon.entry("- **`work run`** (proper noun): the supervisor.", "x")
    assert (t.term, t.category) == ("`work run`", "actor")


def test_an_entry_without_a_category_is_read_with_none():
    t = spec_lexicon.entry("- **status**: an initiative's are `proposed` and `done`.", "spec/index.md")
    assert t.term == "status" and t.category == ""
    assert spec_lexicon.entry("not an entry", "x") is None


def test_a_category_of_plugin_2_names_no_part_of_speech_and_relabel_gives_it():
    for old, new in [("kind", "noun"), ("actor", "proper noun"), ("event", "verb"),
                     ("condition of stage", "adjective of stage"), ("attribute of stage", "attribute of stage"),
                     ("resource, exclusive", "noun, exclusive"),
                     ("resource, counted by `workers`", "noun, counted by `workers`")]:
        assert spec_lexicon.relabel(old) == new
        before, after = (spec_lexicon.entry("- **x** (%s): a thing." % w, "x") for w in (old, new))
        assert (before.category == "attribute") == (old == new) and after.category in spec_lexicon.CATEGORIES
    assert spec_lexicon.relabel("noun") is None and spec_lexicon.relabel("relation a → b") is None
    lex = spec_lexicon.Lexicon([spec_lexicon.entry("- **stage** (kind): a thing.", "spec/index.md")])
    assert ("v_t4", "stage", "spec/index.md: the term does not name its part of speech; (kind) is written (noun)") \
        in spec_lexicon.problems(lex)


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
        - **initiative** (noun): one.
        - **initiative** (noun): twice.
        - **phase** (attribute of initiative): Values: `a`, `b`.
        - **state** (attribute of initiative): Values: `b`, `c`.
        - **colour** (attribute of balloon): Values: `red`.
        - **a session** (proper noun): clashes with the kind.
        - **session** (noun): a conversation.
        - **print** (verb): a core verb of the grammar.
    """)
    codes = sorted((p[0], p[1]) for p in spec_lexicon.problems(lex))
    assert ("v_t4", "colour") in codes and ("v_t4", "status") in codes
    assert ("v_t5", "`b`") in codes
    assert ("v_t6", "initiative") in codes and ("v_t6", "a session") in codes and ("v_t6", "print") in codes


def _codes(glossary, code):
    return [p[1] for p in spec_lexicon.problems(_lexicon(glossary)) if p[0] == code]


def test_v_t7_a_gloss_is_one_sentence():
    """design-r2 §8's counting rule: code spans, quotes and e.g./i.e./etc./vs. are blanked first; `.!?` before a space
    or the end, and `;`, end a sentence; `:` does not; fields after the gloss are not counted."""
    passing = """
        - **index** (noun): the file `spec/index.md. x` of a context.
        - **brief** (noun): what a worker reads, e.g. the work-item and its tests.
        - **ledger** (noun): the record of an initiative: its runs and their costs.
        - **initiative** (noun): the delivery of one request. Plural: initiatives. Not: epic.
        - **quoted** (noun): a line "that says. this" of a file.
        - **status** (attribute of initiative): Values: `proposed`, `done`.
    """
    assert _codes(passing, "v_t7") == []
    failing = """
        - **brief** (noun): what a worker reads. It names the work-item.
        - **log** (noun): what a round writes; one line a step.
        - **pool** (noun): the workers! Every one.
    """
    assert sorted(_codes(failing, "v_t7")) == ["brief", "log", "pool"]


def test_v_t9_a_means_field():
    assert _codes("- **open** (adjective of initiative): Means: its status is not `done`.\n"
                  "- **initiative** (noun): one.", "v_t9") == ["open"]
    assert _codes("- **open** (adjective of initiative): an initiative is open when the initiative is not `done`.\n"
                  "- **initiative** (noun): one.", "v_t9") == []


def test_the_definition_of_a_condition_is_its_gloss():
    lex = _lexicon("""
        - **initiative** (noun): one. Kind of: node.
        - **node** (noun): a thing.
        - **open** (adjective of initiative): An initiative is open when the initiative is not `done`.
    """)
    assert lex.definition("open") == "An initiative is open when the initiative is not `done`."
    assert lex.definition(lex.of("condition")[0]) == lex.definition("open")
    assert lex.definition("initiative") == "" and lex.definition("nothing") == ""
    assert lex.of("kind")[0].supertype == "node"
    assert spec_lexicon.gloss("Values: `a`, `b`.") == ""


def test_same_named_conditions_have_their_own_definitions():
    lex = _lexicon("""
        - **initiative** (noun): one.
        - **work-item** (noun): one.
        - **open** (adjective of initiative): An initiative is open when the initiative is not `done`.
        - **open** (adjective of work-item): A work-item is open when the work-item is not `green`.
    """)
    initiative, item = sorted(lex.of("condition"), key=lambda t: t.kinds)
    assert lex.definition(item) == "A work-item is open when the work-item is not `green`."
    assert lex.definition(initiative) == "An initiative is open when the initiative is not `done`."


def test_words_are_every_spelling_a_line_may_use():
    words = spec_lexicon.read(FIXTURE).words()
    assert {"`work run`", "initiative", "`drafted`", "spec lock", "under"} <= words


def test_a_4_0_entry_gives_a_verbs_aspect_and_frames_and_a_kinds_this():
    t = spec_lexicon.entry("- **write** (verb, action): an agent puts text into a file. Forms: writes, written. "
                           "Frame: agent writes text. Frame: agent writes text to file.", "x")
    assert (t.category, t.aspect, t.frame) == ("event", "action", "agent writes text")
    assert t.frames == ("agent writes text", "agent writes text to file")
    assert spec_lexicon.entry("- **name** (verb, state): a text holds a name. Frame: text names thing.", "x").aspect \
        == "state"
    assert spec_lexicon.entry("- **name** (verb): a thing named. Frame: text names thing.", "x").aspect == ""
    assert spec_lexicon.entry("- **name** (verb, wish): a thing named.", "x").category == ""
    t = spec_lexicon.entry("- **session** (noun): a conversation. This: the session the command runs in.", "x")
    assert (t.category, t.this) == ("kind", "the session the command runs in")
