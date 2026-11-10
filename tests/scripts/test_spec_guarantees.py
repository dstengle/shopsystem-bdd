"""The guarantees capabilities, converted (the GF conversion's design §16, plan P9): each file is codified, every
statement parses to exactly one tree in the live `Req` grammar, `model logic` finds no error in it (the one live run,
`live_logic`, less its known findings), `model
restates` finds every 0.29 id restated, dropped or moved, and none of them has a feature file. Of the 11 converted,
only `trials` is left; the others are retired in 2.0.0 (test_spec_retired)."""
import pathlib
import re
import sys

import model_restates
import pytest
import spec_grammar
import spec_grammar4
import spec_language
import spec_lexicon
import spec_lf
import spec_read
import spec_solve
import spec_tree

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
RECORDS = REPO / ".shop" / "records" / "2026-11-03-gf-conversion"
GUARANTEES = ("trials",)


def path(cap):
    return REPO / "spec" / "capabilities" / f"{cap}.md"


def four(cap):
    return spec_read.codified(path(cap), (spec_read.MARKER4,))


@pytest.fixture(scope="module")
def grammar():
    toolchain.require()
    return spec_grammar.load(REPO)


@pytest.mark.parametrize("cap", GUARANTEES)
def test_the_capability_is_codified_and_well_formed(cap):
    assert spec_read.codified(path(cap)), f"{cap} has no `language: codified-1` or `codified-2`"
    doc = spec_read.capability(path(cap))
    assert doc.problems == []
    assert doc.groups, f"{cap} has no group"
    assert doc.frontmatter.get("group") == "guarantees"


@pytest.mark.parametrize("cap", GUARANTEES)
def test_every_statement_parses_to_one_tree(grammar, cap):
    refused = []
    for g in spec_read.capability(path(cap)).groups:
        for r in g.requirements:
            p = spec_language.parse(REPO, r.text, capability=cap)    # in its file's grammar (CNL 4's I19)
            if p.tree is None:
                refused.append(f"{cap}#{r.id}: {p.refusal}: {r.text}")
    assert refused == []


@pytest.mark.live_logic
@pytest.mark.parametrize("cap", GUARANTEES)
def test_the_logic_check_finds_no_error(live_logic, live_expected, cap):
    errors = [f.text for f in live_logic if f.code in spec_solve.ERRORS and any(i.startswith(f"{cap}#") for i in f.ids)
              and not live_expected(f)]
    assert errors == []


@pytest.mark.parametrize("cap", GUARANTEES)
def test_every_old_id_is_restated_dropped_or_moved(cap):
    rows = model_restates.coverage(REPO, cap)
    assert rows, f"spec/restated.json has no id of {cap}"
    assert [r["id"] for r in rows if r["state"] == "missing"] == []


@pytest.mark.parametrize("cap", GUARANTEES)
def test_a_guarantees_capability_has_no_feature(cap):
    assert not (REPO / "features" / f"{cap}.feature").exists()


def test_the_lexicon_has_no_problem(grammar):
    assert spec_lexicon.problems(spec_lexicon.read(REPO)) == []


@pytest.mark.parametrize("cap", GUARANTEES)
def test_each_group_is_one_statement_numbered_as_its_group(cap):
    """Revision 2 (design-r2 §9.1): one statement for each group, and g<n> and r<n> share n."""
    odd = [(g.id, [r.id for r in g.requirements]) for g in spec_read.capability(path(cap)).groups
           if [r.id for r in g.requirements] != ["r" + g.id[1:]]]
    assert odd == []


@pytest.mark.parametrize("cap", GUARANTEES)
def test_no_two_groups_share_features_condition_and_trigger(grammar, cap):
    """v15n: statements that share features, condition and trigger are one statement (design-r2 §9.1); of a codified-1
    file, as model check reads v15n (a codified-2 line gives it no `pre`)."""
    seen, shared = {}, []
    for g in spec_read.capability(path(cap)).groups if not four(cap) else ():
        for r in g.requirements:
            clauses = spec_tree.parts(spec_tree.normal(spec_grammar.parse(REPO, r.text).tree))
            if all(clauses[k] is None for k in ("feat", "cond", "trig")):
                continue
            key = tuple("-" if clauses[k] is None else spec_tree.show(clauses[k]) for k in ("feat", "cond", "trig"))
            if seen.setdefault(key, g.id) != g.id:
                shared.append((seen[key], g.id))
    assert shared == []


@pytest.mark.parametrize("cap", GUARANTEES)
def test_the_id_map_gives_every_id_the_capability_has(cap):
    """ids-<cap>.tsv (design-r2 §9.1): old codified id, tab, new id; its new ids are exactly the file's, or, once the
    file is reworded in the new language (CNL 4's I23a), each of them is the file's, live or retired."""
    rows = [line.split("\t") for line in (RECORDS / f"ids-{cap}.tsv").read_text().splitlines()]
    olds = [old for old, _ in rows]
    assert len(olds) == len(set(olds))
    doc = spec_read.capability(path(cap))
    have = {f"{cap}#{x}" for g in doc.groups for x in [g.id] + [r.id for r in g.requirements]}
    if four(cap):
        assert {new for _, new in rows} <= have | {f"{cap}#{x}" for x in doc.retired}
    else:
        assert {new for _, new in rows} == have


@pytest.mark.parametrize("u, acts", [("U12", ["exit", "change"]), ("U13", ["commit", "push"])])
def test_u12_and_u13_are_one_statement_of_joined_verb_phrases(u, acts):
    """U12 (U11 reworded in grammar 4) and U13 (U4) by VP coordination: one `shall`, its acts joined by `and`, each
    done by the one subject."""
    toolchain.require()
    text = {c.id: c.text for c in spec_read.universal(REPO)}[u]
    tree = spec_language.parse(REPO, text, universal=True).tree
    shown = spec_lf.show(spec_lf.form(spec_grammar4.load(REPO)[0], tree))
    found = re.findall(r"(\w+)\(e\d+, subject: (x\d+)", shown.split("response", 1)[1])
    assert [act for act, _ in found] == acts and len({subject for _, subject in found}) == 1
