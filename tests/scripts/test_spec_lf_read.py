"""The reading rules R1-R12 (the CNL 4 design, call 5, section 7.3; I11b): each block of grammar/language.md read by
grammar 4 as the block says (its logical form, or the refusal of spec_lf_read), and the refusals of R2, R4, R8 and
R12 printed by `model parse` with the line's tree."""
import pathlib
import re
import subprocess
import sys

import pytest
import spec_grammar4
import spec_lf
import spec_lf_read

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "codified-2"
LANGUAGE = REPO / "grammar" / "language.md"
BLOCK = re.compile(r"^```reading\n(.*?)\n```$", re.MULTILINE | re.DOTALL)


@pytest.fixture(scope="module")
def vocab():
    toolchain.require()
    return spec_grammar4.load(FIXTURE)[0]


def reading(vocab, line, root=FIXTURE):
    """What grammar 4 reads a line as in a context (the fixture's unless `root` names another): its refusal, else its
    logical form as `model parse --form` prints it."""
    p = spec_grammar4.parse(root, line)
    if not p.tree:
        return p.refusal
    return spec_lf_read.refusal(vocab, p.tree) or spec_lf.show(spec_lf.form(vocab, p.tree))


def blocks():
    return [b.split("\n", 1) for b in BLOCK.findall(LANGUAGE.read_text())]


def test_every_rule_of_the_language_reference_has_its_blocks():
    text = LANGUAGE.read_text()
    assert [int(n) for n in re.findall(r"^## R(\d+)\. ", text, re.MULTILINE)] == list(range(1, 13))
    assert len(blocks()) >= 20


@pytest.mark.parametrize("line, said", blocks())
def test_each_line_of_the_language_reference_reads_as_it_says(vocab, line, said):
    assert reading(vocab, line) == said


def test_the_refusals_name_the_words(vocab):
    said = reading(vocab, "When the person runs `work start`, `work` shall print the stage.")
    assert said.startswith('refused: "the stage" has no antecedent')
    said = reading(vocab, "While sessions do not follow stages, when the person runs `work start`, `work` shall "
                          "exit successfully.")
    assert 'says "does not follow stages"' in said and '"follows no stage"' in said
    said = reading(vocab, "While a session does not have a worktree, when the person runs `work start`, `work` "
                          "shall exit successfully.")
    assert '"has no worktree"' in said and '"a worktree that the session does not have"' in said


def test_the_restricted_the_binds_to_an_earlier_referent_and_keeps_its_restriction(vocab):
    f = spec_lf.form(vocab, spec_grammar4.parse(FIXTURE, "When a session ends a stage, `work` shall print the stage "
                                                         "that a session follows.").tree)
    response = f.parts[-1]
    assert [r.kind for r in response.refs] == ["session"]
    assert any(getattr(a, "pred", None) == "state" for a in response.body)


def test_model_parse_prints_a_reading_refusal_with_the_tree_and_exits_1():
    model = [sys.executable, str(REPO / "scripts" / "model"), "--root", str(FIXTURE), "parse"]
    done = subprocess.run(model + ["`work` shall write a file."], capture_output=True, text=True)
    assert done.returncode == 1, done.stdout + done.stderr
    assert done.stdout.startswith('refused: the line has no trigger and neither "always" nor "never"')
    assert "  tree: " in done.stdout
    done = subprocess.run(model + ["--form", "`work` shall not write a file."], capture_output=True, text=True)
    assert done.returncode == 0 and "not [x2: file]" in done.stdout, done.stdout + done.stderr
