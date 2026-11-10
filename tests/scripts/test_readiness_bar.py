"""readiness r1-r4 (workflow simplification plan 3, Task 2, D6-D9): `work ready` checks the bar on a copy of `spec/`
with the item's lines laid in, readies a passing item and names every reason an item is not passing; `spec/` itself
is never written."""
import os
import pathlib
import sys

import backlog_items
import pytest
import readiness_bar
from backlog_testing import git, state, work, write_item
from spec_solve import Finding
from test_backlog_lines import ABANDON, DONE, FROBNICATE, TERM

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

# An L3 alone: no transition takes a `proposed` initiative to `abandoned`. The fixture's DONE gives an L1 with r1 too.
SKIPS = ("While an initiative is `proposed`, when the person runs `work abandon` on the initiative, `work` shall set the status of the initiative to "
         "`abandoned`.")
GUARANTEE = "An initiative always fulfils a request."


@pytest.fixture
def shaped(ready_repo):
    toolchain.require()
    write_item(ready_repo, "b1", status="shaped")
    return ready_repo


def line(repo, text, *flags, into="work-queue"):
    done = work(repo, "line", "b1", "--into", into, *flags, text)
    assert done.returncode == 0, done.stderr


def test_ready_readies_a_passing_item(shaped):
    line(shaped, ABANDON)
    done = work(shaped, "ready", "b1")
    assert done.returncode == 0, done.stderr
    assert done.stdout == 'b1 "Fix the parser" ready\n'
    assert backlog_items.find(shaped, "b1").status == "ready"
    assert git(shaped, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b1.md"]
    assert git(shaped, "log", "-1", "--format=%s").strip() == 'work ready: b1 "Fix the parser" shaped -> ready'


def test_a_line_that_does_not_parse_is_the_reason(shaped):
    line(shaped, FROBNICATE)
    before = state(shaped)
    done = work(shaped, "ready", "b1")
    assert done.returncode == 1, done.stdout
    assert 'work ready: b1 "Fix the parser" is not passing:' in done.stderr
    for word in ("work-queue#r5", "frobnicate", "parsed up to:"):
        assert word in done.stderr, done.stderr
    assert state(shaped) == before


def test_an_item_with_no_lines_is_not_passing(shaped):
    before = state(shaped)
    done = work(shaped, "ready", "b1")
    assert done.returncode == 1 and "work line" in done.stderr, done.stderr
    assert state(shaped) == before


def test_ready_refuses_an_item_that_is_not_shaped_before_checking(ready_repo):
    write_item(ready_repo, "b1", status="idea")
    line(ready_repo, FROBNICATE)
    done = work(ready_repo, "ready", "b1")
    assert done.returncode == 1
    assert 'b1 "Fix the parser" is idea' in done.stderr and "frobnicate" not in done.stderr, done.stderr


def test_every_reason_is_named(shaped):
    line(shaped, FROBNICATE)
    line(shaped, FROBNICATE.replace("frobnicate the initiative", "frobnicate the work-item"), "--group", "Another")
    done = work(shaped, "ready", "b1")
    assert done.returncode == 1
    reasons = [x for x in done.stderr.splitlines() if x.startswith("  ")]
    assert [r.split(":")[0] for r in reasons] == ["  work-queue#r5", "  work-queue#r6"], done.stderr


@pytest.mark.parametrize("finding, refuses", [
    (Finding("L1", ["supervision#r1", "supervision#r2"], "elsewhere"), False),
    (Finding("L1", ["work-queue#r5", "work-queue#r1"], "the item's"), True),
    (Finding("L0", [], "the check did not finish"), True),
    (Finding("L3", ["work-queue#r5"], "a transition"), False),
])
def test_only_the_items_l0_and_l1_refuse(shaped, monkeypatch, finding, refuses):
    line(shaped, ABANDON)
    monkeypatch.setattr(readiness_bar.spec_solve, "run", lambda *_args, **_kwargs: [finding])
    reasons, warnings = readiness_bar.well_formed(shaped, backlog_items.find(shaped, "b1"))
    assert reasons == (["%s %s" % (finding.code, finding.text)] if refuses else [])
    assert warnings == (["L3 a transition"] if finding.code == "L3" else [])


def test_an_l3_is_a_warning(shaped):
    line(shaped, SKIPS)
    done = work(shaped, "ready", "b1")
    assert done.returncode == 0, done.stderr
    assert "work ready: warning:" in done.stderr and "L3" in done.stderr, done.stderr


def test_an_l1_naming_the_items_line_refuses(shaped):
    line(shaped, DONE)
    done = work(shaped, "ready", "b1")
    assert done.returncode == 1 and "L1 work-queue#r1 and #r5 clash" in done.stderr, done.stderr


def test_a_guarantees_line_is_not_generated(shaped, monkeypatch):
    """plan-3 review M3: `features generate` is never run on a guarantees capability."""
    line(shaped, GUARANTEE, into="review")

    def generate(*_args):
        raise readiness_bar.features_generate.GenerateError("generated")
    monkeypatch.setattr(readiness_bar.features_generate, "generate", generate)
    assert readiness_bar.well_formed(shaped, backlog_items.find(shaped, "b1")) == ([], [])


def test_a_line_with_the_items_term_readies(shaped):
    """plan-3 review M4: a missing word written as the item's own term bullet (D4)."""
    assert work(shaped, "line", "b1", "--into", "work-queue", "--term", TERM).returncode == 0
    line(shaped, FROBNICATE)
    done = work(shaped, "ready", "b1")
    assert done.returncode == 0, done.stderr


def test_an_l1_elsewhere_does_not_refuse_on_the_solver(shaped):
    """plan-3 review M4: an L1 between lines of spec/ alone, unstubbed, does not refuse an unrelated item."""
    path = shaped / "spec" / "capabilities" / "work-queue.md"
    path.write_text(path.read_text().replace("## Not yet", "### [g4] Done\n- [r5] %s\n\n## Not yet" % DONE, 1))
    git(shaped, "commit", "-qam", "an L1 in spec/")
    assert any(f.code == "L1" and "work-queue#r5" in f.ids for f in readiness_bar.spec_solve.run(shaped))
    line(shaped, ABANDON)
    done = work(shaped, "ready", "b1")
    assert done.returncode == 0, done.stderr


@pytest.mark.parametrize("text, code", [(ABANDON, 0), (FROBNICATE, 1)])
def test_ready_never_writes_spec_and_cleans_up(shaped, tmp_path, monkeypatch, text, code):
    line(shaped, text)
    temp = tmp_path / "temp"
    temp.mkdir()
    monkeypatch.setitem(os.environ, "TMPDIR", str(temp))
    done = work(shaped, "ready", "b1")
    assert done.returncode == code, done.stderr
    assert git(shaped, "status", "--porcelain", "--", "spec") == ""
    assert git(shaped, "status", "--porcelain") == ""
    assert list(temp.iterdir()) == []


def test_a_group_generate_skips_is_the_reason(shaped, monkeypatch):
    """plan-3 review M5: the groups `features generate` writes no scenario for are read off `skipped`, not stderr."""
    fg = readiness_bar.features_generate
    steps = fg.features_generate4.spec_steps4
    monkeypatch.setattr(steps, "cases", lambda *_a: (_ for _ in ()).throw(steps.TraceError("no step")))
    skipped = {}
    fg.generate(shaped, shaped / "spec" / "capabilities" / "work-queue.md", skipped)
    assert skipped == {"work-queue#g%d" % n: "no step" for n in (1, 2, 3)}
    line(shaped, ABANDON)
    reasons, _ = readiness_bar.well_formed(shaped, backlog_items.find(shaped, "b1"))
    assert reasons == ["work-queue#g4 has no scenario: no step"]
