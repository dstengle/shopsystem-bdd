"""The revision's "Done means" (design-r2 §2, plan-r2 R14) measured on the live repository, and what R14 deletes."""
import dataclasses
import json
import re
import resource
import subprocess
import sys
import time
from pathlib import Path

import pytest
import spec_lexicon
import spec_rgl_vocab

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"


def run(*args, **kw):
    return subprocess.run([sys.executable, *map(str, args)], cwd=ROOT, capture_output=True, text=True, **kw)


@pytest.fixture(scope="module")
def check():
    """`model check` of the live repository, once: its tests are one xdist group, on one worker."""
    done = run(SCRIPTS / "model", "check", "--json")
    return json.loads(done.stdout)


def rules(found, *codes):
    return [row for row in found["violations"] + found["warnings"] if row[0] in codes]


@pytest.mark.xdist_group("model_check")
def test_no_given_line_that_is_not_example_data(check):
    """Point 1: v15m has no rows."""
    assert rules(check, "v15m") == []


@pytest.mark.xdist_group("model_check")
def test_no_two_statements_share_a_trigger_and_a_condition(check):
    """Point 2: v15k, v15l and v15n have no rows."""
    assert rules(check, "v15k", "v15l", "v15n") == []


def test_the_live_lexicon_has_no_problem_and_the_spec_no_means():
    """Point 3: v_t4-v_t10 have no rows (the lexicon read with the kinds of its packs, as `model check` reads it), and
    no capability or index says `Means:`."""
    assert spec_lexicon.problems(spec_lexicon.read(ROOT), spec_rgl_vocab.outer(ROOT)) == []
    assert [p for p in (ROOT / "spec").rglob("*.md") if "Means:" in p.read_text()] == []


def test_a_term_has_no_means_field():
    assert "means" not in {f.name for f in dataclasses.fields(spec_lexicon.Term)}


INDEX = """\
---
id: bounded-context/ex.com/p/ctx
language: codified-1
---

## Glossary

- **work-item** (noun): a unit of work.
- **capability-proposal** (noun): a proposal of one capability.
- **under** (relation work-item → capability-proposal): a work-item delivers part of a proposal.
- **for** (relation work-item → capability-proposal): the proposal a work-item is for.
"""


def test_a_relation_entry_is_v_t8_and_gives_no_relation(tmp_path):
    """A relation is a row of `## Relations`; an entry, whatever its word, is the legacy form, refused."""
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "index.md").write_text(INDEX)
    lex = spec_lexicon.read(tmp_path)
    assert lex.relations() == []
    assert sorted(p[:2] for p in spec_lexicon.problems(lex) if p[0] == "v_t8") == [("v_t8", "for"), ("v_t8", "under")]


def test_no_fixed_horizon():
    """Point 4: no horizon constant."""
    assert [p.name for p in SCRIPTS.glob("*.py") if "HORIZON = " in p.read_text()] == []


def test_no_commits_step():
    """`SCommits` and its Then are gone: a commit and its push are two conjuncts, two Thens."""
    files = list((ROOT / "grammar").glob("*.gf")) + list(SCRIPTS.glob("*.py")) + list(
        (ROOT / "tests" / "scenarios").glob("*.py"))
    assert [p.name for p in files if re.search(r"SCommits|ThenCommits", p.read_text())] == []
    assert [p.name for p in (ROOT / "features").glob("*.feature") if "and pushes the commit" in p.read_text()] == []


def test_every_script_module_has_a_map_row():
    """Point 7: every `scripts/*.py` is named in CLAUDE.md's module map, by name or by a `<prefix>*` row."""
    text = (ROOT / "CLAUDE.md").read_text()
    missing = [p.name for p in sorted(SCRIPTS.glob("*.py"))
               if p.name not in text and "%s*" % p.name.split("_")[0] not in text]
    assert missing == []


def test_the_lines_of_q47_parse(tmp_path):
    """Point 6: a request raised with `work request` is read by the new grammar: its lines are work-queue's, a
    codified-1 capability, so they are parsed in its grammar now that the index says codified-2 (b151)."""
    text = (ROOT / ".shop" / "work" / "requests" / "q47.md").read_text()
    body = text.split("## Lines", 1)[1].split("## Questions", 1)[0]
    lines = [re.sub(r"^\d+\. ", "", l) for l in body.splitlines() if re.match(r"^\d+\. ", l)]
    assert len(lines) == 6
    (tmp_path / "q47.txt").write_text("\n".join(lines) + "\n")
    done = run(SCRIPTS / "model", "parse", "--capability", "work-queue", "--file", tmp_path / "q47.txt")
    assert done.returncode == 0, done.stdout + done.stderr


@pytest.mark.live_logic
def test_model_logic_finds_no_conflict_in_the_spec(live_logic, live_expected):
    """Point 4 on the live spec: no L1-L3 finding outside the known ones (`EXPECTED`); L4 and L5 are warnings."""
    assert [f.text for f in live_logic if f.code in ("L1", "L2", "L3") and not live_expected(f)] == []


@pytest.mark.live_logic
def test_every_known_finding_still_fires(live_logic):
    """An `EXPECTED` entry whose finding is gone (its question answered, or the check fixed) is removed."""
    from conftest import EXPECTED
    assert sorted(set(EXPECTED) - {" ".join([f.code] + list(f.ids)) for f in live_logic}) == []


def _cpu():
    used = resource.getrusage(resource.RUSAGE_CHILDREN)
    return used.ru_utime + used.ru_stime


@pytest.mark.live_logic
@pytest.mark.timing
def test_model_logic_on_the_live_spec_is_fast():
    """design-r3 §6: the whole context in one solve, in under 2 s. Measured as the run's CPU time, which is its wall
    time on an idle machine (plan-r3 S12 timed 1.1 s of each). Under a full xdist load the CPU time of one run
    inflates (2.5 s at 32 workers), so it is a `timing` test, left out of the parallel run and run alone with
    `python3 -m pytest -m timing -n 0` (workflow simplification plan-3 review S5); the best of up to three runs."""
    best = None
    for _ in range(3):
        start, wall = _cpu(), time.monotonic()
        done = run(SCRIPTS / "model", "logic", "--json", timeout=60)
        took, wall = _cpu() - start, time.monotonic() - wall
        best = took if best is None else min(best, took)
        if best < 2:
            break
    took = best
    assert "Traceback" not in done.stderr, done.stderr
    assert took < 2, "model logic took %.1f s of CPU (%.1f s wall)" % (took, wall)


@pytest.mark.live_logic
def test_the_live_logic_tests_share_one_worker(request):
    """plan-r3 S12: the live solve is once per worker, so every `live_logic` test is one xdist group, on one worker
    (`--dist loadgroup`), and the live spec is solved once a run, not once a worker."""
    assert request.node.get_closest_marker("xdist_group").args == ("live_logic",)
    assert "--dist loadgroup" in " ".join(request.config.getini("addopts"))
