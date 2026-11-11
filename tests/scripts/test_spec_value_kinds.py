"""spec_value_kinds (b257): an attribute's values declared adjectives or nouns, the short form "x is `v`" refused of
a noun value with the full form in its hint, and an attribute that declares neither read as in 4.0."""
import pathlib
import shutil

import pytest

import spec_grammar4
import spec_lexicon
import spec_value_kinds
import toolchain

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "codified-2"


def test_an_entry_declares_its_values_adjectives_or_nouns():
    t = spec_lexicon.entry("- **status** (attribute of item): Values (adjective): `shaped`, `ready`. "
                           "Values (noun): `idea`, `needs-input`.", "x")
    assert t.values == ("`shaped`", "`ready`", "`idea`", "`needs-input`")
    assert dict(t.value_kinds) == {"`shaped`": "adjective", "`ready`": "adjective", "`idea`": "noun",
                                   "`needs-input`": "noun"}
    assert spec_value_kinds.kind(t, "`idea`") == "noun" and spec_value_kinds.kind(t, "`ready`") == "adjective"
    t = spec_lexicon.entry("- **tier** (attribute of decision): Values (noun): `check`, `judgement`. Order: as "
                           "listed.", "x")
    assert t.values == ("`check`", "`judgement`") and t.order == "as listed"


def test_a_plain_values_field_declares_no_kind():
    t = spec_lexicon.entry("- **size** (attribute of item): Values: `small`, `large`.", "x")
    assert t.values == ("`small`", "`large`") and t.value_kinds == ()
    assert spec_value_kinds.kind(t, "`small`") == "" and spec_value_kinds.undeclared(t)


def test_a_code_no_entry_lists_is_a_noun_of_an_attribute_that_declares_its_kinds():
    t = spec_lexicon.entry("- **release** (attribute of repo): Values (noun): `1.0.0`. Order: by number.", "x")
    assert spec_value_kinds.kind(t, "`1.0.1`") == "noun"
    t = spec_lexicon.entry("- **release** (attribute of repo): Values: `1.0.0`. Order: by number.", "x")
    assert spec_value_kinds.kind(t, "`1.0.1`") == ""


def test_values_and_a_declared_field_on_one_entry_is_a_problem(tmp_path):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "index.md").write_text(
        "# x\n## Glossary\n- **item** (noun): a piece of work.\n"
        "- **status** (attribute of item): Values: `a`. Values (noun): `b`.\n")
    found = [p for p in spec_lexicon.problems(spec_lexicon.read(tmp_path)) if p[1] == "status"]
    assert found and found[0][0] == "v_t4" and "Values" in found[0][2]


@pytest.fixture(scope="module")
def root():
    toolchain.require()
    return FIXTURE


@pytest.mark.parametrize("line, value, full", [
    ("While a stage is `review`, when the person runs `work start`, `work` shall end the stage.", "`review`",
     'the tier of the stage is `review`'),
    ("While a stage is not `check`, when the person runs `work start`, `work` shall end the stage.", "`check`",
     'the tier of the stage is not `check`'),
    ("While a stage is one of `check` or `review`, when the person runs `work start`, `work` shall end the stage.",
     "`check`", 'the tier of the stage is one of'),
    ("While a file is `1.0.1`, when the person runs `work start`, `work` shall print the file.", "`1.0.1`",
     'the version of the file is `1.0.1`'),
])
def test_the_short_form_of_a_noun_value_is_refused_naming_the_full_form(root, line, value, full):
    p = spec_grammar4.parse(root, line)
    assert p.tree is None and p.refusal.startswith("refused: %s is a noun" % value), p.refusal
    assert full in p.refusal and ("whose" in p.refusal) == (" one of " not in line)


@pytest.mark.parametrize("line", [
    "While the tier of a stage is `review`, when the person runs `work start`, `work` shall end the stage.",
    "When a session ends a stage whose tier is `check`, `work` shall print the stage.",
    "While a stage is `open`, when the person runs `work start`, `work` shall end the stage.",
    "While the version of a file is `1.0.1`, when the person runs `work start`, `work` shall print the file.",
])
def test_the_full_form_and_an_adjective_values_short_form_parse(root, line):
    assert spec_grammar4.parse(root, line).tree, spec_grammar4.parse(root, line).refusal


def test_an_undeclared_attribute_keeps_the_short_form(tmp_path, root):
    shutil.copytree(FIXTURE, tmp_path / "ctx")
    index = tmp_path / "ctx" / "spec" / "index.md"
    index.write_text(index.read_text().replace("Values (noun): `check`", "Values: `check`"))
    line = "While a stage is `review`, when the person runs `work start`, `work` shall end the stage."
    assert spec_grammar4.parse(tmp_path / "ctx", line).tree
