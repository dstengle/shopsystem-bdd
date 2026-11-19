"""spec_vocabulary and spec_vocabulary_terms: a context's words named onto its domain model (the domain contract
design, §4.2), their layers and problems (v_t18-v_t21), and the lexicon the grammars read from them."""
import pathlib
import shutil

import pytest

import spec_lexicon
import spec_packs
import spec_relations
import spec_rgl_vocab
import spec_vocabulary

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"
CODIFIED = pathlib.Path(__file__).parent / "fixtures" / "codified-2"


@pytest.fixture
def ctx(tmp_path):
    shutil.copytree(FIXTURE, tmp_path, dirs_exist_ok=True)
    return tmp_path


def _add(root, area, text):
    path = root / "spec" / "vocabulary" / ("%s.md" % area)
    path.write_text(path.read_text() + text if path.exists() else "---\narea: %s\n---\n\n%s" % (area, text))


def _codes(root, code):
    return [term for c, term, _ in spec_vocabulary.problems(root) if c == code]


def test_each_element_kind_is_resolved():
    by_term = {e.term: e.element for e in spec_vocabulary.entries(FIXTURE)}
    assert by_term["note"].kind == "object" and by_term["note"].id == "note"
    assert by_term["status"].kind == "attribute" and by_term["status"].id == "note.status"
    assert by_term["draft"].kind == "value" and by_term["draft"].id == "note.status draft"
    assert by_term["carry"].kind == "relation" and by_term["carry"].id == "note.carries"
    assert by_term["add"].kind == "operation" and by_term["add"].id == "notes.add"
    assert by_term["the notes service"].kind == "service"
    assert by_term["the person"].kind == "actor"
    assert {e.layer for e in spec_vocabulary.entries(FIXTURE)} == {"notes", "shared"}


def test_the_fixture_has_no_problem():
    assert spec_vocabulary.problems(FIXTURE) == []


def test_v_t18_an_entry_that_names_no_element(ctx):
    _add(ctx, "notes", "- **shelf** (noun): a place notes are kept.\n")
    assert _codes(ctx, "v_t18") == ["shelf"]


def test_v_t19_an_entry_naming_an_element_the_model_does_not_declare(ctx):
    _add(ctx, "notes", "- **shelf** (noun) → object shelf.\n- **mark** (verb, action) → operation notes.mark.\n")
    assert _codes(ctx, "v_t19") == ["mark", "shelf"]


def test_v_t20_two_entries_of_one_layer_naming_one_element(ctx):
    _add(ctx, "notes", "- **memo** (noun) → object note.\n- **notes** (noun) → object note.\n")
    assert _codes(ctx, "v_t20") == ["memo"]       # "notes" is the plural of "note", a form of it


def test_v_t20_in_two_layers_is_no_problem(ctx):
    _add(ctx, "archive", "- **memo** (noun) → object note.\n")
    assert _codes(ctx, "v_t20") == []


def test_v_t21_the_retired_cli_import_waits_for_the_request_pack(ctx, monkeypatch):
    index = ctx / "spec" / "index.md"
    index.write_text(index.read_text().replace("imports: []", "imports: [cli]"))
    monkeypatch.setattr(spec_vocabulary, "REQUEST_PACK", ctx / "no-such-pack.md")
    assert _codes(ctx, "v_t21") == []
    monkeypatch.setattr(spec_vocabulary, "REQUEST_PACK", index)
    assert _codes(ctx, "v_t21") == ["cli"]


def test_an_area_reads_its_own_layer_its_imports_and_shared(ctx):
    model = ctx / "spec" / "model"
    (model / "archive.md").write_text("---\narea: archive\nkind: supporting\nimports: [notes]\n---\n\n"
                                      "```model\nobject shelf\n```\n")
    assert spec_vocabulary.layers_of(ctx, "archive") == ["archive", "notes", "shared"]
    assert spec_vocabulary.layers_of(ctx, "notes") == ["notes", "shared"]


def test_the_lexicon_comes_from_the_model():
    lex = spec_lexicon.read(FIXTURE)
    kinds = {t.term for t in lex.of("kind")}
    assert kinds == {"note", "tag"}
    status = next(t for t in lex.of("attribute") if t.term == "status")
    assert status.kinds == ("note",)
    assert status.value_kinds == (("`draft`", "adjective"), ("`active`", "adjective"), ("`retired`", "adjective"))
    assert status.transitions == (("`draft`", "`active`", ""), ("`active`", "`retired`", ""),
                                  ("`draft`", "`retired`", ""))
    actors = {t.term: t.supertype for t in lex.of("actor")}
    assert actors == {"the person": "agent", "the notes service": "agent"}
    frames = {t.term: t.frames for t in lex.of("event")}
    assert frames["carry"] == ("note carries tag",)
    assert frames["add"] == ("agent adds note",)
    assert {(r.k1, r.word, r.k2, r.cardinality) for r in lex.rows} == {("tag", "of", "note", "one")}
    assert spec_lexicon.problems(lex, spec_rgl_vocab.outer(FIXTURE)) == []


def test_relations_are_read_from_the_model():
    assert [(r.k1, r.word, r.k2) for r in spec_relations.read(FIXTURE)] == [("tag", "of", "note")]


def test_the_area_layers_follow_the_packs():
    layers = {layer for layer, _ in spec_packs.layers(FIXTURE)}
    assert layers == {"area notes", "area shared"}


def test_a_word_of_two_areas_gives_one_term_each(ctx):
    model = ctx / "spec" / "model"
    (model / "analysis.md").write_text("---\narea: analysis\nkind: generic\n---\n\n```model\n"
                                       "object lint finding\n```\n")
    (model / "notes.md").write_text((model / "notes.md").read_text().replace(
        "object tag\n", "object finding\n\nobject tag\n"))
    _add(ctx, "notes", "- **finding** (noun) → object finding.\n")
    _add(ctx, "analysis", "- **finding** (noun) → object lint finding.\n")
    vocab = spec_rgl_vocab.read(ctx)
    assert vocab.nouns["finding_notes"] == ("finding", "findings")
    assert vocab.nouns["finding_analysis"] == ("finding", "findings")
    assert "finding" not in vocab.kinds


def test_a_context_without_a_model_reads_as_today():
    lex = spec_lexicon.read(CODIFIED)
    assert {t.term for t in lex.of("kind")} >= {"file", "stage", "worktree"}
    assert all(t.word == "" for t in lex.terms)
    assert spec_vocabulary.problems(CODIFIED) == []
    assert all(not layer.startswith("area ") for layer, _ in spec_packs.layers(CODIFIED))


def test_the_fixtures_lines_read_in_its_vocabulary():
    import spec_language
    import spec_read
    cap = spec_read.capability(FIXTURE / "spec" / "capabilities" / "notebook.md")
    lines = [r.text for g in cap.groups for r in g.requirements]
    assert len(lines) == 2
    for line in lines:
        parsed = spec_language.parse(FIXTURE, line)
        assert parsed.tree and not parsed.refusal, (line, parsed.refusal)


def test_the_fixture_passes_model_check_and_its_features_are_current():
    import subprocess
    import sys
    scripts = pathlib.Path(__file__).resolve().parents[2] / "scripts"
    check = subprocess.run([sys.executable, str(scripts / "model"), "check"], cwd=FIXTURE, capture_output=True,
                           text=True)
    assert check.stdout.strip().endswith("0 violations, 0 warnings, 0 unresolved references, 0 file problems"), \
        check.stdout
    features = subprocess.run([sys.executable, str(scripts / "features"), "generate", "--check"], cwd=FIXTURE,
                              capture_output=True, text=True)
    assert features.returncode == 0, features.stdout + features.stderr
