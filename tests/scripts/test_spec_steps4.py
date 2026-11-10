"""Steps from the logical form (the CNL 4 design, I14a): `features generate` on a codified-2 capability writes each
group's steps off its requirements' forms in the step grammar 4, byte-stable; every step it writes reads back through
that grammar into the one tree it was written from and the template a handler is keyed by; a Then a universal
condition entails is left out with a comment naming it; a construct with no step skips its group."""
import pathlib
import subprocess
import sys

import features_vocab4
import pytest
import spec_rgl_steps

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world as C
import toolchain

FEATURES = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "features"
LINES = ["When the person runs `work backlog` with the `--json` option, `work` shall exit successfully.",
         ("While a session follows a stage, if the person runs `work start`, then `work` shall exit with an error "
          "naming the stage."),
         "When sessions write a file, `work` shall print the file.",
         "When the person runs this command, `work` shall print this command.",
         ("If the person runs `work start`, then `work` shall exit with an error naming `work start` and change "
          "nothing."),
         "While a session follows a stage, the session shall not write a file.",
         "When the person runs `work start`, `work` shall print at least two stages.",
         "A session may write a file."]


@pytest.fixture(scope="module")
def world(tmp_path_factory):
    toolchain.require()
    repo = tmp_path_factory.mktemp("steps4")
    C.context(repo, "ex.com/prod/ctx", LINES, "c1", C.UNIVERSAL["declining"])
    return repo


def generate(repo):
    return subprocess.run([sys.executable, str(FEATURES), "generate", "c1"], cwd=repo, capture_output=True, text=True)


def scenarios(repo):
    text = (repo / "features" / "c1.feature").read_text()
    return {part.split("\n", 1)[0]: part for part in text.split("  @")[1:]}


def steps(scenario):
    """(keyword, text) of each step, And read as the keyword before it."""
    out, last = [], None
    for line in scenario.splitlines():
        word, _, rest = line.strip().partition(" ")
        if word in ("Given", "When", "Then", "And"):
            last = word.lower() if word != "And" else last
            out.append((last, rest))
    return out


def test_generate_is_byte_stable_and_skips_a_group_no_step_words(world):
    first = generate(world)
    assert first.returncode == 0, first.stderr
    text = (world / "features" / "c1.feature").read_text()
    again = generate(world)
    assert again.returncode == 0 and (world / "features" / "c1.feature").read_text() == text
    assert "c1#g7: no scenario: no Then of count" in first.stderr
    assert "c1#g8: no scenario: no step of a line that says may" in first.stderr
    assert sorted(scenarios(world)) == ["g%d @r%d" % (k, k) for k in range(1, 7)]


def test_the_steps_of_each_form(world):
    generate(world)
    found = {k: steps(v) for k, v in scenarios(world).items()}
    assert found["g1 @r1"] == [("when", "the person runs `work backlog` with `--json`"),
                               ("then", "`work` exits successfully")]
    assert found["g2 @r2"] == [("given", "a session s1"), ("given", "a stage s2"),
                               ("given", "the session s1 follows the stage s2"),
                               ("when", "the person runs `work start`"),
                               ("then", "`work` exits with an error naming the stage s2")]
    assert found["g4 @r4"] == [("when", "the person runs this command"), ("then", "`work` prints this command")]
    assert found["g6 @r6"][-1] == ("then", "the session s1 does not write a file")


def test_an_entailed_then_is_left_out_with_its_premise(world):
    generate(world)
    g5 = scenarios(world)["g5 @r5"]
    assert steps(g5) == [("when", "the person runs `work start`"),
                         ("then", "`work` exits with an error naming `work start`")]
    assert g5.rstrip().endswith("    # entailed: U1 through the definition of refuse")


def test_every_step_reads_back_into_its_tree_and_template(world):
    generate(world)
    read = {}
    for scenario in scenarios(world).values():
        for keyword, text in steps(scenario):
            call = features_vocab4.step(world, keyword, text)
            assert spec_rgl_steps.text(spec_rgl_steps.load(world)[1], call.tree) == text
            read[text] = (call.template, call.term, call.names, call.nps)
    assert read["the person runs `work start`"][:2] == ("WhenRuns", "`work start`")
    assert read["`work` exits with an error naming the stage s2"] == ("ThenExitsErr", "`work`", ["s2"],
                                                                      ["the stage s2"])
    assert read["a stage s2"][:3] == ("GivenK", "stage", ["s2"])
    assert read["the session s1 follows the stage s2"][:2] == ("GivenDoes", "follow")
    assert read["the session s1 does not write a file"][:2] == ("ThenDoesNot", "write")
    assert read["`work` prints the file f1"][:2] == ("ThenPrints", "`work`")


def test_a_step_of_no_reading_is_refused(world):
    with pytest.raises(features_vocab4.StepError):
        features_vocab4.step(world, "then", "`work` sings the stage s1")


def test_a_given_of_example_data_reads_back_as_grammar_3s(world):
    """b218: "the K `n` holds:" (its block under the step) is GivenCodeText, "the K `n` holds" and one value GivenCode,
    as a codified-1 step of example data reads, its kind the term."""
    gram = spec_rgl_steps.load(world)[1]
    for text, template, quoted in (("the file `a.txt` holds:", "GivenCodeText", []),
                                   ('the file `a.txt` holds "3.0.0"', "GivenCode", ['"3.0.0"']),
                                   ("the file `a.txt` holds `3.0.0`", "GivenCode", ["`3.0.0`"])):
        call = features_vocab4.step(world, "given", text)
        assert spec_rgl_steps.text(gram, call.tree) == text
        assert (call.template, call.kind, call.term, call.names, call.quoted) == (template, "file", "file",
                                                                                  ["`a.txt`"], quoted)
