"""`measure defect` (telemetry r3; workflow simplification plan 7, D11): a fault found after the merge written against
its delivered item and its merged batch, committed alone, numbered on, and counted in its own batch's measurement
only; anything else refused, changing nothing."""
import datetime

import batch_plan
import measure_defect
import pytest
from backlog_testing import git, state, work, write_item
from measure_read import Refused
from review_testing import ok, published
from test_batch_tasks import resumed
from test_measure_batch import figures, measure, merged, store  # noqa: F401  (the fixtures)

TODAY = datetime.date.today().isoformat()


def test_a_defect_is_written_and_committed(merged):  # noqa: F811
    done = measure(merged, "defect", "b1", "--says", "the fault")
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == ".shop/batches/1/defect-1.md"
    rel = ".shop/batches/1/defect-1.md"
    found = measure_defect.parse((merged / rel).read_text(), rel)
    assert found == measure_defect.Defect("d1", "defect/ex.com/prod/ctx/batch-1/d1", "batch-1", "b1", TODAY,
                                          "the fault")
    assert git(merged, "log", "-1", "--format=%s").strip() == 'measure defect: batch-1 d1 of b1 "Abandon"'
    assert git(merged, "show", "--name-only", "--format=", "HEAD").split() == [rel]
    assert git(merged, "status", "--porcelain") == ""


@pytest.fixture
def in_review(batch_repo, request):
    request.getfixturevalue("store")
    published(batch_repo)
    return batch_repo


def abandon(repo):
    from batch_testing import ready_item
    from test_backlog_lines import ABANDON
    from test_batch_pick import SECOND
    ready_item(repo, "b1", "Abandon", ABANDON)
    ready_item(repo, "b2", "Exit", SECOND)
    ok(work(repo, "batch", "start"))
    resumed(repo)
    ok(work(repo, "batch", "abandon", "batch-1"))
    write_item(repo, "b1", title="Abandon", status="delivered")   # by hand: only the batch's status refuses it


@pytest.mark.parametrize("case, item, says, named", [
    ("in-review", "b2", "the fault", "in-batch"),
    ("merged", "b3", "the fault", "no batch"),
    ("abandoned", "b1", "the fault", "abandoned"),
    ("merged", "b1", "  ", "--says"),
])
def test_a_defect_needs_a_delivered_item_of_a_merged_batch(request, batch_repo, case, item, says, named):
    """Review Focus 4."""
    if case == "in-review":
        repo = request.getfixturevalue("in_review")
    elif case == "abandoned":
        request.getfixturevalue("store")
        abandon(batch_repo)
        repo = batch_repo
    else:
        repo = request.getfixturevalue("merged")
        write_item(repo, "b3", title="Another", status="ready")
    before = state(repo)
    done = measure(repo, "defect", item, "--says", says)
    assert done.returncode == 1, done.stdout
    assert named in done.stderr, done.stderr
    assert done.stderr.startswith("measure defect: ") and done.stderr.count("measure") == 1, done.stderr  # review M9
    assert state(repo) == before


def test_an_unknown_item_is_refused_naming_the_command(merged):  # noqa: F811
    """Plan 7 review M9: the subcommand is named once."""
    done = measure(merged, "defect", "b9", "--says", "the fault")
    assert done.returncode == 1 and done.stderr.startswith("measure defect: ") and "b9" in done.stderr, done.stderr


def test_the_next_defect_is_numbered_on(merged):  # noqa: F811
    """Review Focus 4."""
    for k in (1, 2):
        done = measure(merged, "defect", "b1", "--says", "fault %d" % k)
        assert done.stdout.strip() == ".shop/batches/1/defect-%d.md" % k, done.stderr
    assert [d.name for d in measure_defect.defects(merged, "batch-1")] == ["d1", "d2"]
    git(merged, "rm", "-q", ".shop/batches/1/defect-1.md")
    git(merged, "commit", "-q", "-m", "d1 removed by hand")
    done = measure(merged, "defect", "b1", "--says", "fault 3")
    assert done.stdout.strip() == ".shop/batches/1/defect-3.md", (done.stdout, done.stderr)


def test_a_defect_round_trips():
    d = measure_defect.Defect("d3", "defect/ex.com/prod/ctx/batch-2/d3", "batch-2", "b4", "2026-11-05", "it breaks\n\nrun x")
    rel = measure_defect.rel_of("batch-2", 3)
    assert rel == ".shop/batches/2/defect-3.md"
    assert measure_defect.parse(measure_defect.render(d), rel) == d
    with pytest.raises(Refused, match="kind"):
        measure_defect.parse(measure_defect.render(d).replace("kind: defect", "kind: bug"), rel)


def test_a_defect_counts_in_its_own_batch_only(merged):  # noqa: F811
    """Review Focus 4."""
    ok(measure(merged, "defect", "b1", "--says", "the fault"))
    ok(measure(merged, "batch", "batch-1"))
    found = figures(merged)
    assert found["defects"]["after_merge"] == {"b1": 1}
    assert found["defects"]["per_item"] == 1.0 and found["goals"]["defects_per_item"] == 1.0
    write_item(merged, "b3", title="Another", status="in-batch", commit=False)
    head = git(merged, "rev-parse", "HEAD").strip()
    second = batch_plan.Batch("batch-2", "batch/ex.com/prod/ctx/batch-2", "building", "main", head, "batch-2", None,
                              [batch_plan.Task("t1", "b3", "pending", "batch-2-b3")])
    path = merged / batch_plan.rel_of("batch-2")
    path.parent.mkdir(parents=True)
    path.write_text(batch_plan.render(second))
    git(merged, "add", "-A")
    git(merged, "commit", "-q", "-m", "batch-2 by hand")
    ok(measure(merged, "batch", "batch-2"))
    rel = ".shop/records/measurements/%s-batch-2.md" % TODAY
    assert figures(merged, rel)["defects"]["after_merge"] == {}
