"""An artifact in the lexicon (b240 phase 4; b241 holds the rest): the part of speech (artifact), its optional
`Schema:` (schema type and file), and the `Field of:` marker on an attribute or a relation row, read and stored."""
import textwrap

import spec_lexicon
import spec_relations
import spec_rgl_vocab

INDEX = """\
---
id: bounded-context/ex.com/p/ctx
language: codified-2
imports: [cli]
---

## Glossary

- **the comment form** (artifact): the fields of a request comment. Schema: json schema, `schemas/comment.json`.
- **requirement grammar** (artifact): the sentences a context's lines may be.
- **comment** (noun): a remark on an issue.
- **status** (attribute of comment): Values: `open`, `closed`. Field of: the comment form.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| comment | on | comment | one | Field of: the comment form |
| comment | of | comment | Field of: the comment form |
| comment | with | comment |  |
"""


def context(tmp_path):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "index.md").write_text(textwrap.dedent(INDEX))
    return tmp_path


def test_an_artifact_named_with_the_is_a_proper_noun_of_kind_artifact(tmp_path):
    lex = spec_lexicon.read(context(tmp_path))
    form = next(t for t in lex.terms if t.term == "the comment form")
    assert (form.category, form.supertype, form.label) == ("actor", "artifact", "artifact")
    assert form.schema == ("json schema", "schemas/comment.json")
    assert spec_lexicon.gloss(form.text) == "the fields of a request comment."


def test_an_artifact_named_without_the_is_a_noun_under_artifact_and_needs_no_schema(tmp_path):
    lex = spec_lexicon.read(context(tmp_path))
    grammar = next(t for t in lex.terms if t.term == "requirement grammar")
    assert (grammar.category, grammar.supertype, grammar.schema) == ("kind", "artifact", ())


def test_an_attribute_and_a_relation_row_keep_the_artifact_they_are_a_field_of(tmp_path):
    lex = spec_lexicon.read(context(tmp_path))
    assert next(t for t in lex.terms if t.term == "status").field_of == "the comment form"
    rows = {r.word: r for r in spec_relations.read(tmp_path)}
    assert (rows["on"].cardinality, rows["on"].field_of) == ("one", "the comment form")
    assert (rows["of"].cardinality, rows["of"].field_of) == ("", "the comment form")
    assert (rows["with"].cardinality, rows["with"].field_of) == ("", "")


def test_grammar_4_reads_an_artifact_as_an_actor_or_a_kind_under_the_cli_packs_artifact(tmp_path):
    vocab = spec_rgl_vocab.read(context(tmp_path))
    assert vocab.kinds["artifact"] == "thing" and vocab.kinds["requirement grammar"] == "artifact"
    assert ("the comment form", "artifact") in vocab.actors
    assert any(v.term.term == "conform" and v.aspect == "state" for v in vocab.verbs)


def test_an_artifact_and_its_markers_raise_no_problem(tmp_path):
    root = context(tmp_path)
    assert spec_lexicon.problems(spec_lexicon.read(root), spec_rgl_vocab.outer(root)) == []
