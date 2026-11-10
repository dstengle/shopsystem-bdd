"""spec_relations: the `## Relations` tables, `Kind of:` expanded, and the problems v_t8 and v_t10 (design-r2 §4.2, §8)."""
import textwrap

import spec_lexicon
import spec_relations

INDEX = """\
---
id: bounded-context/ex.com/p/ctx
language: codified-1
---

## Glossary

- **node** (noun): a thing work is done on.
- **work-item** (noun): a unit of work. Kind of: node.
- **initiative** (noun): the delivery of one request. Kind of: node.
- **stage** (noun): one session's part of the work.
- **result** (noun): what a stage gives.
- **question** (noun): what a stage asks.

## Relations

| from | word | to |
|---|---|---|
| stage | for | node |
| stage | with | result |
| question | on | node | many |
"""

CAP = """\
---
id: capability/ex.com/p/ctx/sup
---

## Terms

## Relations

| from | word | to |
|---|---|---|
| result | asks | question |
"""


def repo(tmp_path, index=INDEX, cap=CAP):
    (tmp_path / "spec" / "capabilities").mkdir(parents=True)
    (tmp_path / "spec" / "index.md").write_text(index)
    (tmp_path / "spec" / "capabilities" / "sup.md").write_text(cap)
    return spec_lexicon.read(tmp_path)


def test_rows_are_read_from_the_index_and_from_a_capability(tmp_path):
    rows = repo(tmp_path).rows
    assert [(r.k1, r.word, r.k2, r.where) for r in rows] == [
        ("stage", "for", "node", "spec/index.md"), ("stage", "with", "result", "spec/index.md"),
        ("question", "on", "node", "spec/index.md"), ("result", "asks", "question", "spec/capabilities/sup.md")]
    assert rows[2].cardinality == "many" and rows[0].cardinality == ""


def test_kind_of_is_read_as_the_supertype(tmp_path):
    supertypes = {t.term: t.supertype for t in repo(tmp_path).of("kind")}
    assert supertypes["work-item"] == "node" and supertypes["stage"] == ""


def test_a_row_naming_a_supertype_expands_to_each_subkind_and_keeps_its_own(tmp_path):
    rels = repo(tmp_path).relations()
    fors = sorted((k1, w, k2) for k1, w, k2, _ in rels if w == "for")
    assert fors == [("stage", "for", "initiative"), ("stage", "for", "node"), ("stage", "for", "work-item")]
    assert len({rid for _, w, _, rid in rels if w == "for"}) == 1, "one relation id for the row"
    assert ("question", "on", "work-item") in {r[:3] for r in rels}


def test_a_relation_entry_is_no_row_and_is_v_t8(tmp_path):
    cap = CAP.replace("## Terms\n", "## Terms\n\n- **gives** (relation result → question): a question the result gives.\n")
    lex = repo(tmp_path, cap=cap)
    rels = {r[:3] for r in lex.relations()}
    assert ("result", "gives", "question") not in rels and ("result", "asks", "question") in rels
    assert [p[:2] for p in spec_lexicon.problems(lex) if p[0] == "v_t8"] == [("v_t8", "gives")]


def test_v_t8_a_relation_entry_that_names_a_preposition_too(tmp_path):
    cap = CAP.replace("## Terms\n", "## Terms\n\n- **for** (relation stage → result): the result a stage is for.\n")
    found = spec_lexicon.problems(repo(tmp_path / "a", cap=cap))
    assert [p[:2] for p in found if p[0] == "v_t8"] == [("v_t8", "for")]
    assert not [p for p in spec_lexicon.problems(repo(tmp_path / "b")) if p[0] == "v_t8"]


def test_v_t10_two_rows_with_one_from_word_and_to(tmp_path):
    found = [p for p in spec_lexicon.problems(repo(tmp_path / "a", index=INDEX + "| stage | for | work-item |\n"))
             if p[0] == "v_t10"]
    assert len(found) == 1 and "stage for work-item" in found[0][2]
    assert not [p for p in spec_lexicon.problems(repo(tmp_path / "b")) if p[0] == "v_t10"]


def test_a_row_or_a_supertype_naming_no_kind_is_v_t4(tmp_path):
    index = INDEX.replace("Kind of: node.", "Kind of: thing.", 1) + "| stage | under | balloon |\n"
    found = [p for p in spec_lexicon.problems(repo(tmp_path, index=index)) if p[0] == "v_t4"]
    assert [p for p in found if "balloon" in p[2]] and [p for p in found if "thing" in p[2]]


def test_rows_of_a_table_skip_its_header_and_rule_and_end_with_the_section():
    text = textwrap.dedent("""\
        ## Relations

        | from | word | to |
        |---|---|---|
        | a | b | `c` |

        ## Next
        | x | y | z |
        """)
    assert [(r.k1, r.word, r.k2) for r in spec_relations.rows(text, "w")] == [("a", "b", "c")]
