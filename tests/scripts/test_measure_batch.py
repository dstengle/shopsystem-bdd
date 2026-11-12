"""`measure batch` (telemetry r1, r2; workflow simplification plan 7, D2-D10): a batch's window from git, its sessions'
requests inside it read from the root's own project directory in Claude Code's store, each session's role and session
time, the cost by role, the pull request's findings by grade, and the knobs it ran with, written as one record."""
import datetime
import json
import subprocess
import sys

import batch_plan
import measure_batch
import measure_batch_read
import measure_batch_sessions as S
import measure_cost
import pytest
from backlog_testing import SCRIPTS, git, work
from batch_templates import templated
from measure_batch_testing import store_rows, write_agent, write_session
from review_testing import FIX_NOW_B1, FIXED_F1, findings, ok, published
from test_batch_close import merge
from test_batch_fix_loop import fix

TODAY = datetime.date.today().isoformat()
RECORD = ".shop/records/measurements/%s-batch-1.md" % TODAY
DAY = datetime.timedelta(days=1)


@pytest.fixture
def store(tmp_path, monkeypatch):
    """Claude Code's store of the test's own: never the person's."""
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "store"))
    return tmp_path / "store"


def reviewed_once(repo):
    published(repo)
    ok(work(repo, "batch", "brief", "batch-1"))
    findings(repo).write_text(FIX_NOW_B1)
    ok(work(repo, "batch", "reviewed", "batch-1"))


@pytest.fixture
def merged(batch_repo, store):
    """batch-1 reviewed with a fix-now finding on b1, fixed, reviewed clean, merged into main and `merged`: built once
    a worker and copied into the test's own repository and outside directory (batch_templates)."""
    templated(batch_repo, "merged", merging)
    return batch_repo


def merging(repo, outside):
    reviewed_once(repo)
    fix(repo)
    ok(work(repo, "batch", "review", "batch-1"))
    ok(work(repo, "batch", "brief", "batch-1"))
    findings(repo, 2).write_text(FIXED_F1)
    ok(work(repo, "batch", "reviewed", "batch-1"))
    merge(repo, outside)
    ok(work(repo, "batch", "merged", "batch-1"))


def measure(repo, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / "measure"), *args], cwd=repo, capture_output=True,
                          text=True, timeout=60)


def figures(repo, rel=RECORD):
    return json.loads((repo / rel).read_text().split("```json\n", 1)[1].split("\n```", 1)[0])


def times(repo):
    """The commit times of the batch's plan, oldest first."""
    return git(repo, "log", "--reverse", "--format=%cI", "--", ".shop/batches/1/plan.md").split()


def at(text):
    return datetime.datetime.fromisoformat(text)


def iso(moment):
    return moment.isoformat()


def project(repo):
    return measure_batch_read.project_dir(repo)


def test_a_merged_batch_is_measured(merged):
    done = measure(merged, "batch", "batch-1")
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == RECORD
    text = (merged / RECORD).read_text()
    for words in ("wall time", "session time", "tokens", "cost by role"):
        assert words in text, words
    found = figures(merged)
    assert found["batch"] == "batch-1" and found["status"] == "merged"
    assert [i["item"] for i in found["items"]] == ["b1", "b2"]
    assert all(found["window"][k] for k in ("started", "first_review", "built", "closed"))
    assert found["wall_time_seconds"] >= 0
    assert list(found)[:3] == ["batch", "status", "pull_request"]


def test_the_findings_are_counted_by_grade(merged):
    ok(measure(merged, "batch", "batch-1"))
    found = figures(merged)
    assert found["findings_by_grade"] == {"Critical": 0, "Important": 1, "Minor": 1}
    assert found["defects"]["review"] == {"b1": 1}
    assert found["reviews"][0]["result"] == "fix-now"
    assert "Important" in (merged / RECORD).read_text()


T0 = datetime.datetime(2026, 11, 5, 10, 0, tzinfo=datetime.UTC)
REVIEW = T0 + datetime.timedelta(hours=1)


def one(agent=None, minutes=10):
    when = T0 + datetime.timedelta(minutes=minutes)
    return measure_batch_read.Request("q-%s-%d" % (agent, minutes), "s", agent, when, "claude-opus-5-5", 1, 0, 0, 0, 1)


@pytest.mark.parametrize("agent, kind, minutes, review, role", [
    (None, (None, None), 10, REVIEW, "planning"),
    ("a1", ("shopsystem-bdd:pr-reviewer", None), 10, REVIEW, "review"),
    ("a1", ("general-purpose", "batch-1 review 2"), 10, REVIEW, "review"),
    ("a1", ("general-purpose", "batch-1 fix f1"), 10, REVIEW, "fixing"),
    ("a1", ("general-purpose", "batch-1 t2 b2"), 90, REVIEW, "implementing"),
    ("a1", (None, None), 10, REVIEW, "implementing"),
    ("a1", (None, None), 90, REVIEW, "fixing"),
    ("a1", (None, None), 90, None, "implementing"),
])
def test_each_session_has_its_role(agent, kind, minutes, review, role):
    """Review Focus 3: D6's four rules, the first that applies."""
    types = {"a1": kind} if agent else {}
    (found,) = S.sessions_of([one(agent, minutes)], types, (T0, T0 + DAY), review, measure_cost.PRICES, batch="batch-1")
    assert found["role"] == role


def test_only_the_windows_requests_count(merged):
    """Review Focus 1."""
    moments = times(merged)
    start, end = at(moments[0]), at(moments[-2])
    write_session(project(merged), "m", store_rows("m", [iso(start - DAY), moments[0], moments[-2], iso(end + DAY)]))
    write_agent(project(merged), "m", "a1", store_rows("m", [moments[1], iso(end + DAY)], agent="a1"))
    write_agent(project(merged), "m", "a2", store_rows("m", [iso(start - DAY), moments[1]], agent="a2"))
    ok(measure(merged, "batch", "batch-1"))
    by = {(s["session"], s["agent"]): s for s in figures(merged)["sessions"]}
    assert set(by) == {("m", None), ("m", "a1")}
    assert by["m", None]["requests"] == 2
    gap = (end - start).total_seconds()
    assert gap <= S.IDLE and by["m", None]["session_time_seconds"] == round(gap)
    assert by["m", "a1"]["requests"] == 2


def test_session_time_leaves_out_idle_gaps():
    requests = [measure_batch_read.Request("q%d" % s, "s", None, T0 + datetime.timedelta(seconds=s), "m", 0, 0, 0, 0, 1)
                for s in (0, 60, 120, 1000)]
    (found,) = S.sessions_of(requests, {}, (T0, T0 + DAY), None, measure_cost.PRICES)
    assert found["session_time_seconds"] == 120


def test_only_the_roots_project_directory_is_read(merged, store):
    """Review Focus 1."""
    other = store / "projects" / "-somewhere-else"
    write_session(other, "o", store_rows("o", [times(merged)[1]]))
    ok(measure(merged, "batch", "batch-1"))
    assert figures(merged)["sessions"] == []
    ok(measure(merged, "batch", "batch-1", "--sessions", str(other), "--replace"))
    assert [s["session"] for s in figures(merged)["sessions"]] == ["o"]


def test_a_batch_with_no_transcripts_is_measured_without_sessions(merged):
    """Review Focus 1."""
    done = measure(merged, "batch", "batch-1")
    assert done.returncode == 0, done.stderr
    found = figures(merged)
    assert found["sessions_found"] == 0 and found["sessions_from"] == str(project(merged))
    assert "no transcripts at" in (merged / RECORD).read_text()


def test_the_cost_by_role_sums_to_the_cost(merged):
    moments = times(merged)
    write_session(project(merged), "m", store_rows("m", [moments[0]]))
    for agent, description, moment in (("a1", "batch-1 t1 b1", moments[1]), ("a2", "batch-1 review 1", moments[2]),
                                       ("a3", "batch-1 fix f1", moments[3])):
        write_agent(project(merged), "m", agent, store_rows("m", [moment], agent=agent), "general-purpose", description)
    write_agent(project(merged), "m", "a4", store_rows("m", [moments[1]], agent="a4", model="claude-new-9"))
    ok(measure(merged, "batch", "batch-1"))
    found = figures(merged)
    roles = found["cost_by_role"]
    assert list(roles) == list(S.ROLES) and all(roles[r]["sessions"] >= 1 for r in S.ROLES)
    assert round(sum(r["cost"] for r in roles.values()), 6) == round(found["cost"], 6) and found["cost"] > 0
    assert found["unpriced"] == {"claude-new-9": 1}
    assert "batch-1 t1" not in (merged / RECORD).read_text()


def numstat(repo, rng):
    out = git(repo, "diff", "--numstat", rng, "--", ".", ":(exclude).shop").splitlines()
    return sum(int(a) + int(b) for a, b, _ in (line.split("\t") for line in out) if a != "-")


def test_the_knobs_are_given(merged):
    """Plan 7 review S1 and the rulings' Q3: the changed lines are the whole batch as last reviewed, its fork to the
    last review's head; each review keeps its own range's lines."""
    ok(measure(merged, "batch", "batch-1"))
    found = figures(merged)
    record = lambda k, key: (merged / (".shop/batches/1/review-%d.md" % k)).read_text().split(
        key + ": ", 1)[1].split("\n", 1)[0]
    forked = batch_plan.find(merged, "batch-1").forked_from
    want = numstat(merged, "%s..%s" % (forked, record(2, "head")))
    assert want > numstat(merged, record(2, "range")) > 0
    assert found["knobs"] == {"batch_size": 4, "items": 2, "changed_lines": want, "size_limit": 1000, "reviews": 2,
                              "readiness_bar": "mechanical"}
    assert [r["lines"] for r in found["reviews"]] == [numstat(merged, record(k, "range")) for k in (1, 2)]


def test_an_open_batch_is_measured_so_far(batch_repo, store, monkeypatch):
    published(batch_repo)
    started = at(times(batch_repo)[0])
    monkeypatch.setattr(measure_batch, "now", lambda: started + datetime.timedelta(hours=2))
    found = measure_batch.figures_of(batch_repo, "batch-1")
    assert found["status"] == "in-review" and found["window"]["closed"] is None
    assert found["wall_time_seconds"] == 7200 and found["waiting_for_merge_seconds"] is None


def test_a_measurement_is_not_written_over(merged):
    ok(measure(merged, "batch", "batch-1"))
    before = (merged / RECORD).read_text()
    done = measure(merged, "batch", "batch-1")
    assert done.returncode == 1 and RECORD in done.stderr, done.stderr
    assert (merged / RECORD).read_text() == before
    ok(measure(merged, "batch", "batch-1", "--replace"))


def test_an_unknown_batch_is_refused(merged):
    done = measure(merged, "batch", "batch-9")
    assert done.returncode == 1 and "batch-9" in done.stderr, done.stderr
    assert not (merged / ".shop/records/measurements").exists()
