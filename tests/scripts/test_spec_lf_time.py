"""The time constructs (the CNL 4 design, section 4.4, call 9; I16): grammar/corpus/time-4.txt parsed in the
codified-2 context with the time pack (tests/scripts/fixtures/codified-2-time/), their logical form (spec_lf_time),
and `model logic`'s refusal of a line holding one, which the check has no reading of yet."""
import pathlib
import re
import sys

import pytest
import spec_context
import spec_gf
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
        elif spec_grammar4.linearise(FIXTURE, p.tree) != spec_gf.normalise(line):
            failures.append("%s\n    linearises as %s" % (line, spec_grammar4.linearise(FIXTURE, p.tree)))
    assert not failures, "\n".join(failures)


BLOCK = re.compile(r"^```reading-time\n(.*?)\n```$", re.MULTILINE | re.DOTALL)


def blocks():
    """The blocks of grammar/language.md's section on time: a line and what grammar 4 reads it as."""
    return [b.split("\n", 1) for b in BLOCK.findall((REPO / "grammar" / "language.md").read_text())]


def test_the_language_reference_shows_each_time_construct():
    lines = " ".join(line for line, _ in blocks())
    for words in ("within the last", " after ", "the clock reaches", " has written ", " since "):
        assert words in lines, words


@pytest.mark.parametrize("line, said", blocks())
def test_each_time_line_of_the_language_reference_reads_as_it_says(line, said):
    vocab, _ = spec_grammar4.load(FIXTURE)
    p = spec_grammar4.parse(FIXTURE, line)
    assert (p.refusal or spec_lf_read.refusal(vocab, p.tree) or spec_lf.show(spec_lf.form(vocab, p.tree))) == said


def world(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines), fixture=codified2_world.TIME_FIXTURE)
    return tmp_path


def refused(tmp_path, *lines):
    """What `model logic`'s reading of the context refuses each line of `lines` with, by id."""
    return spec_context.load(world(tmp_path, *lines)).refused


def test_model_logic_refuses_a_comparison_of_moments_by_name(tmp_path):
    out = refused(tmp_path, "While a deadline is within the last 7 days, " + ON + "print the deadline.",
                  "While a deadline is not before `2026-01-01`, " + ON + "exit successfully.")
    assert set(out) == {"thing#r1", "thing#r2"}, out
    assert all("no translation of a comparison of moments" in why for why in out.values()), out


def test_model_logic_refuses_a_history_by_name(tmp_path):
    out = refused(tmp_path, "While a session has ended a stage, when the session writes a file, `work` shall print "
                  "the file.", "While a session has written no file since `2026-01-01`, when the session ends a stage, "
                  "`work` shall exit successfully.")
    assert set(out) == {"thing#r1", "thing#r2"}, out
    assert "no translation of the history of end" in out["thing#r1"], out
    assert "no translation of the history of write" in out["thing#r2"], out


def test_model_logic_reads_no_pair_of_two_refused_time_lines(tmp_path):
    """The bounds of "within the last 30 days" and "not within the last 7 days" leave a moment between them, but the
    check reads neither line, so it finds no L1 of them."""
    found = spec_solve.run(world(tmp_path, "While a deadline is within the last 30 days, " + ON + "print the deadline.",
                                 "While a deadline is not within the last 7 days, " + ON + "not print the deadline."),
                           capability="thing")
    assert [f.code for f in found if f.code == "L1"] == []
