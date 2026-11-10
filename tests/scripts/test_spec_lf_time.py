"""The time constructs (the CNL 4 design, section 4.4, call 9; I16): grammar/corpus/time-4.txt parsed in the
codified-2 context with the time pack (tests/scripts/fixtures/codified-2-time/), their logical form (spec_lf_time),
check.lp's facts of it (spec_lf_facts) and `model logic` over them: comparisons of a moment exact over the constants
named, a history a state relation."""
import pathlib
import re
import sys

import pytest
import spec_context
import spec_grammar
import spec_grammar4
import spec_lf
import spec_lf_read
import spec_solve

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "codified-2-time"
CORPUS = REPO / "grammar" / "corpus" / "time-4.txt"
ON = "when the person runs `work start` on the deadline, `work` shall "


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def corpus():
    """time-4.txt as [(line, the reason it is refused with, or None)], as core-4.txt is read."""
    out = []
    for raw in CORPUS.read_text().splitlines():
        if raw.startswith("= refused: "):
            out[-1] = (out[-1][0], raw[len("= refused: "):].strip())
        elif raw.strip() and not raw.startswith("#"):
            out.append((raw.strip(), None))
    return out


def test_every_line_of_the_time_corpus_has_one_meaning_that_round_trips_or_is_refused_with_its_reason():
    failures, vocab = [], spec_grammar4.load(FIXTURE)[0]
    for line, reason in corpus():
        p = spec_grammar4.parse(FIXTURE, line)
        refusal = p.refusal or spec_lf_read.refusal(vocab, p.tree)     # the reading rules' (R4) after the grammar's
        if reason is not None:
            if refusal is None or reason not in refusal:
                failures.append("%s\n    not refused with %r: %s" % (line, reason, refusal or p.tree))
        elif refusal is not None:
            failures.append("%s\n    %s" % (line, refusal))
        elif spec_grammar4.linearise(FIXTURE, p.tree) != spec_grammar.normalise(line):
            failures.append("%s\n    linearises as %s" % (line, spec_grammar4.linearise(FIXTURE, p.tree)))
    assert not failures, "\n".join(failures)


BLOCK = re.compile(r"^```reading-time\n(.*?)\n```$", re.MULTILINE | re.DOTALL)


def blocks():
    """The blocks of grammar/language.md's section on time: a line and what grammar 4 reads it as."""
    return [b.split("\n", 1) for b in BLOCK.findall((REPO / "grammar" / "language.md").read_text())]


def test_the_language_reference_shows_each_time_construct():
    lines = " ".join(line for line, _ in blocks())
    for words in ("within the last", " after ", "the clock reaches", " has written ", " since ", "the newest"):
        assert words in lines, words


@pytest.mark.parametrize("line, said", blocks())
def test_each_time_line_of_the_language_reference_reads_as_it_says(line, said):
    vocab, _ = spec_grammar4.load(FIXTURE)
    p = spec_grammar4.parse(FIXTURE, line)
    assert (p.refusal or spec_lf_read.refusal(vocab, p.tree) or spec_lf.show(spec_lf.form(vocab, p.tree))) == said


def world(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines), fixture=codified2_world.TIME_FIXTURE)
    return tmp_path


def facts(tmp_path, *lines):
    ctx = spec_context.load(world(tmp_path, *lines))
    assert not ctx.refused, ctx.refused
    return [f for s in ctx.statements for f in ctx.facts[s.id]]


def codes(tmp_path, *lines):
    return [f.code for f in spec_solve.run(world(tmp_path, *lines), capability="thing")]


def test_a_comparison_is_a_bound_and_a_history_a_state_relation(tmp_path):
    out = facts(tmp_path, "While a deadline is within the last 7 days and a session has ended a stage, " + ON +
                "print the deadline.", "While a deadline is before `2026-01-01`, " + ON + "exit successfully.")
    assert 'cmp("thing#r1",x1,after,ago(604800),pos).' in out
    assert 'crel("thing#r1",hist(e_end),x2,x3,pos).' in out
    assert 'cmp("thing#r2",x1,before,x2,pos).' in out and 'named("thing#r2",x2,"`2026-01-01`").' in out


def test_bounds_that_leave_no_moment_between_them_never_clash(tmp_path):
    assert codes(tmp_path, "While a deadline is within the last 7 days, " + ON + "print the deadline.",
                 "While a deadline is not within the last 30 days, " + ON + "not print the deadline.") == []
    assert codes(tmp_path, "While a deadline is after `2026-01-01`, " + ON + "print the deadline.",
                 "While a deadline is before `2026-01-01`, " + ON + "not print the deadline.") == []


def test_bounds_that_leave_a_moment_between_them_clash(tmp_path):
    assert codes(tmp_path, "While a deadline is within the last 30 days, " + ON + "print the deadline.",
                 "While a deadline is not within the last 7 days, " + ON + "not print the deadline.") == ["L1"]


def test_a_history_and_its_denial_never_clash(tmp_path):
    assert codes(tmp_path, "While a session has ended a stage, when the session writes a file, `work` shall print "
                 "the file.", "While a session has not ended the stage, when the session writes a file, `work` shall "
                 "not print the file.") == []
