"""Grammar 4 (the CNL 4 design, I7a): the base grammar over the RGL with the generated Context (spec_rgl,
spec_rgl_vocab, spec_grammar4), its corpus twin grammar/corpus/core-4.txt, and `model parse`'s switch on
`language: codified-2`."""
import pathlib
import shutil
import subprocess
import sys

import pytest
import spec_grammar
import spec_grammar4
import spec_rgl_vocab

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "codified-2"
CORPUS = REPO / "grammar" / "corpus" / "core-4.txt"


@pytest.fixture(scope="module")
def root():
    toolchain.require()
    return FIXTURE


def twin():
    """core-4.txt as [(line, the reason it is refused with, or None)]."""
    out = []
    for raw in CORPUS.read_text().splitlines():
        if raw.startswith("= refused: "):
            out[-1] = (out[-1][0], raw[len("= refused: "):].strip())
        elif raw.strip() and not raw.startswith("#"):
            out.append((raw.strip(), None))
    return out


def test_every_line_of_the_twin_has_one_tree_that_round_trips_or_is_refused_with_its_reason(root):
    failures = []
    for line, reason in twin():
        p = spec_grammar4.parse(root, line)
        if reason is not None:
            if p.tree is not None or reason not in p.refusal:
                failures.append("%s\n    not refused with %r: %s" % (line, reason, p.tree or p.refusal))
        elif p.tree is None:
            failures.append("%s\n    %s" % (line, p.refusal))
        elif spec_grammar4.linearise(root, p.tree) != spec_grammar.normalise(line):
            failures.append("%s\n    linearises as %s" % (line, spec_grammar4.linearise(root, p.tree)))
    assert not failures, "\n".join(failures)


def test_the_twin_has_each_form_of_a_line_and_both_numbers():
    lines = [line for line, reason in twin() if reason is None]
    for start in ("When ", "If ", "While ", "Where ", "`work` shall"):
        assert any(line.startswith(start) for line in lines), start
    assert any("When sessions write" in line for line in lines) and any(" does not " in line for line in lines)


def test_a_plural_subject_agrees_through_the_rgl(root):
    plural = spec_grammar4.parse(root, "When sessions write a file, `work` shall print the file.")
    assert "DetPl" in plural.tree and "e_write_action" in plural.tree
    p = spec_grammar4.parse(root, "When sessions writes a file, `work` shall print the file.")
    assert p.refusal == "refused: the verb write does not agree in number with its subject"


def test_the_marker_of_spec_index_says_which_grammar(tmp_path):
    assert spec_grammar4.marked(FIXTURE)
    assert not spec_grammar4.marked(REPO / "tests" / "scripts" / "fixtures" / "glossary")
    assert not spec_grammar4.marked(tmp_path)


def test_the_vocabulary_is_every_layer_with_the_base_kinds():
    vocab = spec_rgl_vocab.read(FIXTURE)
    assert vocab.kinds["thing"] is None and vocab.kinds["agent"] == "thing"
    assert vocab.kinds["tool"] == "agent" and vocab.kinds["session"] == "agent" and vocab.kinds["file"] == "thing"
    assert ("`work`", "tool") in vocab.actors
    verbs = {v.term.term: v for v in vocab.verbs}
    assert {"run", "print", "exit", "write", "follow"} <= set(verbs)
    assert verbs["follow"].aspect == "state" and verbs["write"].aspect == "action"
    assert verbs["run"].frames[1] == ("agent", (((), "command"), (("with",), "option")))
    assert verbs["exit"].frames == (("tool", ((("successfully",), None),)),
                                    ("tool", ((("with", "an", "error", "naming"), "thing"),)))
    assert vocab.ancestors("session") == ["session", "agent", "thing"]


def test_a_word_of_the_glossary_takes_the_place_of_the_packs(tmp_path):
    shutil.copytree(FIXTURE / "spec", tmp_path / "spec")
    index = tmp_path / "spec" / "index.md"
    index.write_text(index.read_text() + "- **print** (verb, action): Redefines: cli. A tool shows a file. "
                                         "Frame: tool prints file.\n")
    prints = [v for v in spec_rgl_vocab.read(tmp_path).verbs if v.term.term == "print"]
    assert [v.frames for v in prints] == [(("tool", (((), "file"),)),)]


def test_a_frame_that_does_not_read_is_left_out():
    kinds = {"agent": "thing", "file": "thing", "thing": None}
    assert spec_rgl_vocab.pieces(["file", "file"], kinds) is None
    assert spec_rgl_vocab.pieces(["file", "to", "file"], kinds) == [((), "file"), (("to",), "file")]


def model(root, *args):
    return subprocess.run([sys.executable, str(REPO / "scripts" / "model"), "--root", str(root), *args],
                          capture_output=True, text=True, timeout=300)


def test_model_parse_reads_a_codified_2_context_in_grammar_4(root):
    done = model(root, "parse", "When sessions write a file, `work` shall print the file.")
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("When NoPre (k_agent_Event")
    done = model(root, "parse", "When sessions writes a file, `work` shall print the file.")
    assert done.returncode == 1 and "the verb write does not agree in number with its subject" in done.stdout
    done = model(root, "parse", "When a session writes a stage, `work` shall print the stage.")
    assert done.returncode == 1 and "parsed up to: When a session writes a" in done.stdout
    assert model(root, "parse", "--grammar", "Def", "A stage is open when it is.").returncode == 2


def test_model_parse_reads_a_codified_2_capability_file_s_requirements(root, tmp_path):
    shutil.copytree(FIXTURE / "spec", tmp_path / "spec")
    cap = tmp_path / "spec" / "capabilities" / "thing.md"
    cap.parent.mkdir()
    cap.write_text("---\nid: capability/x/thing\nlanguage: codified-2\nretired: []\n---\n\n# thing\n\n## Behaviour\n\n"
                   "### [g1] one\n- [r1] When a session writes a file, `work` shall print the file.\n")
    done = model(tmp_path, "parse", "--file", str(cap))
    assert done.returncode == 0 and done.stdout.startswith("12: When NoPre"), done.stdout + done.stderr


def test_the_hint_names_the_terms_gf_s_completion_says_may_follow(root):
    """Only the terms a prefix with them still parses: write's object is a file, a session's verb ends a stage, and
    after `shall` every verb of an act a tool may take; a code literal before them does not let any word in."""
    def follow(line):
        return spec_grammar4.hint(root, line)["follow"]
    assert follow("When a session ends a stage, `work` shall write the") == ["file"]
    assert follow("When the person runs `work start`, `work` shall write a stage.") == ["file"]
    assert follow("When a session ends, `work` shall print the file.") == ["stage"]
    # only "to" may follow: the terms after it, the recipient's among them
    assert "agent" in follow("When the person runs `work start`, `work` shall give a file.")
    assert "write" in follow("When a session ends a stage, `work` shall") and "follow" not in follow(
        "When a session ends a stage, `work` shall")
