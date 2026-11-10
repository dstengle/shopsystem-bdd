"""A command's options in the trigger (b240, construct #12): "runs C with the `--x` option", "with the `--x` and
`--y` options", "... on a K", "... set to v" and "without the `--x` option", read by `model logic` as the command
with each option given (and its code argument) and written by `features generate` as a When that names each option as
the line does, whose Call gives its handler the options (`options`) and the options not given (`without`); each twin
of the construct in grammar/language.md, and of the run's own things, translates to the check's facts and to steps."""
import pathlib
import re
import sys

import features_vocab4
import pytest
import spec_context
import spec_grammar4
import spec_lf
import spec_rgl_steps
import spec_solve
import spec_steps4

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "codified-2"
LINE = "When the person runs `work start`%s, `work` shall %s."
OK, ERROR = "exit successfully", "exit with an error naming `work start`"
SECTIONS = re.compile(r'^### ("runs C with|"the push of the command").*?(?=^### |^## )', re.MULTILINE | re.DOTALL)
BLOCK = re.compile(r"^```reading\n(.*?)\n```$", re.MULTILINE | re.DOTALL)


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def facts(line):
    found, why = spec_context.Four(FIXTURE).facts("thing#r1", line)
    assert why is None, why
    return found[1]


def steps(line):
    vocab, gram = spec_rgl_steps.load(FIXTURE)
    form = spec_lf.form(vocab, spec_grammar4.parse(FIXTURE, line).tree)
    return [(k, spec_rgl_steps.text(gram, t)) for k, t in spec_steps4.read(vocab, [("thing#r1", form)])]


def twins():
    text = (REPO / "grammar" / "language.md").read_text()
    return [b.split("\n", 1)[0] for m in SECTIONS.finditer(text) for b in BLOCK.findall(m.group(0))
            if "\nrefused: " not in b]


def test_the_sections_have_their_twins():
    assert len(twins()) >= 10


@pytest.mark.parametrize("line", twins())
def test_each_twin_translates_to_facts_and_to_steps(line):
    assert facts(line)
    vocab = spec_rgl_steps.load(FIXTURE)[0]
    assert spec_steps4.cases(vocab, [("thing#r1", spec_lf.form(vocab, spec_grammar4.parse(FIXTURE, line).tree))])


@pytest.mark.parametrize("options, command, on", [
    (" with the `--json` option", "`work start` `--json`", "none"),
    (" with the `--source` and `--thread` options", "`work start` `--source` `--thread`", "none"),
    (" with the `--every` option set to `5`", "`work start` `--every` `5`", "none"),
    (" without the `--summary` option", "`work start`", "none"),
    (" with the `--json` option on a stage", "`work start` `--json`", "x4"),
    (" with the `--from` option set to a stage", "`work start` `--from`", "x4"),
])
def test_the_command_a_run_runs_is_its_code_with_each_option_given(options, command, on):
    found = facts(LINE % (options, OK))
    assert 'trig("thing#r1",ran,"%s",a_the_person,%s).' % (command, on) in found, found


def codes(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines))
    ctx = spec_context.load(tmp_path)
    assert not ctx.refused, ctx.refused
    return [f.code for f in spec_solve.run(tmp_path, capability="thing")]


@pytest.mark.parametrize("first, second, clash", [
    (" with the `--json` option", " with the `--json` option", True),
    (" with the `--json` option", "", False),
    (" with the `--json` option", " with the `--every` option", False),
    (" without the `--json` option", "", True),
    (" with the `--every` option set to `5`", " with the `--every` option set to `6`", False),
])
def test_a_line_pairs_with_a_line_on_the_same_command(tmp_path, first, second, clash):
    found = codes(tmp_path, LINE % (first, OK), LINE % (second, ERROR))
    assert ("L1" in found) == clash, found


@pytest.mark.parametrize("options, when", [
    (" with the `--json` option", "the person runs `work start` with the `--json` option"),
    (" with the `--source` and `--thread` options",
     "the person runs `work start` with the `--source` and `--thread` options"),
    (" with the `--every` option set to `5`", "the person runs `work start` with the `--every` option set to `5`"),
    (" without the `--summary` option", "the person runs `work start` without the `--summary` option"),
    (" with the `--json` option on a stage", "the person runs `work start` with the `--json` option on the stage s1"),
    (" with the `--from` option set to a stage",
     "the person runs `work start` with the `--from` option set to the stage s1"),
    (" with the `--json` option and the `--from` option set to a stage",
     "the person runs `work start` with the `--json` option and the `--from` option set to the stage s1"),
    (" with the `--json` option and the `--every` option set to `5`",     # b240 phase 21: the argument kept
     "the person runs `work start` with the `--json` option and the `--every` option set to `5`"),
])
def test_the_when_names_each_option_as_the_line_does(options, when):
    assert ("when", when) in steps(LINE % (options, OK)), steps(LINE % (options, OK))


@pytest.mark.parametrize("when, given, without", [
    ("the person runs `work start` with the `--json` option", [("`--json`", None)], []),
    ("the person runs `work start` with the `--source` and `--thread` options",
     [("`--source`", None), ("`--thread`", None)], []),
    ("the person runs `work start` with the `--every` option set to `5`", [("`--every`", "`5`")], []),
    ("the person runs `work start` with the `--from` option set to the stage s1", [("`--from`", "the stage s1")], []),
    ("the person runs `work start` with the `--json` option and the `--from` option set to the stage s1",
     [("`--json`", None), ("`--from`", "the stage s1")], []),
    ("the person runs `work start` without the `--summary` option", [], ["`--summary`"]),
    ("the person runs `work start`", [], []),
])
def test_the_call_gives_its_handler_the_options(when, given, without):
    call = features_vocab4.step(FIXTURE, "when", when)
    assert (call.template, call.command) == ("WhenRuns", "`work start`")
    assert (call.options, call.without) == (given, without)


@pytest.mark.parametrize("given", [" with the `--from` option set to a stage and the `--json` option",
                                   " with the `--every` option set to `5` and the `--json` option"])
def test_a_set_option_before_an_and_keeps_the_tree_that_translates(given):
    # b240 review: one tree reads "set to (a stage and the `--json` option)", a list no option is set to; it is not kept
    # and it no longer ends the parse in a traceback
    parsed = spec_grammar4.parse(FIXTURE, LINE % (given, OK))
    assert parsed.refusal is None and len(parsed.trees) > 1
    assert ("when", "the person runs `work start`" + given.replace("a stage", "the stage s1")) in steps(LINE % (given, OK))
