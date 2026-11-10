"""Conformance to a named artifact (b240 phase 4, construct #5): `features generate` writes "X conforms to A" and "X
does not conform to A" as Givens of the step grammar 4, each read back into its tree as a state of the CLI pack's verb
conform, and the codified-2 world's handler of that Given records what the scenario says conforms to what."""
import pathlib
import subprocess
import sys

import features_vocab4
import spec_rgl_steps

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world as C
import toolchain
import vocab

FEATURES = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "features"
LINES = [("While a file does not conform to the stage form, when the person runs `work start`, `work` shall print "
          "the file and not write the file."),
         ("While a worktree holds a file that conforms to the layout of the worktree, when the person runs "
          "`work start`, `work` shall print the file.")]


def given(tmp_path):
    toolchain.require()
    C.context(tmp_path, "ex.com/prod/ctx", LINES, "c1")
    done = subprocess.run([sys.executable, str(FEATURES), "generate", "c1"], cwd=tmp_path, capture_output=True,
                          text=True)
    assert done.returncode == 0 and done.stderr == "", done.stderr
    text = (tmp_path / "features" / "c1.feature").read_text()
    return [line.strip().split(" ", 1)[1] for line in text.splitlines() if line.strip().startswith(("Given", "And"))]


def test_a_conformance_is_a_given_that_reads_back_as_a_state_of_conform(tmp_path):
    steps = given(tmp_path)
    assert "the file f1 does not conform to the stage form" in steps
    assert "the file f1 conforms to the layout l1" in steps
    gram = spec_rgl_steps.load(tmp_path)[1]
    for text, template in (("the file f1 does not conform to the stage form", "GivenDoesNot"),
                           ("the file f1 conforms to the layout l1", "GivenDoes")):
        call = features_vocab4.step(tmp_path, "given", text)
        assert spec_rgl_steps.text(gram, call.tree) == text
        assert (call.template, call.term, call.subject) == (template, "conform", text.split(" conform")[0]
                                                            .removesuffix(" does not"))


def test_the_codified_2_world_records_what_conforms_to_what(tmp_path):
    given(tmp_path)
    vocab.load_handlers(pathlib.Path(__file__).resolve().parents[1] / "scenarios")
    context = {}
    for text in ("the file f1 does not conform to the stage form", "the file f1 conforms to the layout l1"):
        call = features_vocab4.step(tmp_path, "given", text)
        call.fixtures = lambda name: {"context": context}[name]
        vocab.lookup(call.template, call.term)(call)
    assert context["conforms"] == {("the file f1", "the stage form"): False, ("the file f1", "the layout l1"): True}
