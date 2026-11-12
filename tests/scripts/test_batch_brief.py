"""`work batch brief` (workflow simplification plan 5, Task 2, D3-D8): what `pr-reviewer` reads of a published batch,
its own commits and change, its items' requirement lines, the judgement decisions, the rules, the size and the runs,
written in the ignored worktrees directory with nothing committed."""
import re

import batch_plan
import pytest
from backlog_testing import git, state, work
from batch_testing import commit_on
from review_testing import findings, ok, published, scratch
from test_backlog_lines import ABANDON
from test_batch_pick import SECOND

CHECKS = 'checks = ["python3 -c \\"print(\'ran\')\\""]\n'


def configure(repo, extra=CHECKS):
    """`extra` in batch_repo's `[review]` table: `checks = [...]` in place of its empty checks, else appended."""
    path = repo / ".shop" / "delivery.toml"
    text = path.read_text()
    path.write_text(text.replace("checks = []\n", extra) if extra.startswith("checks = ") else text + extra)
    git(repo, "commit", "-q", "-am", "review checks")


@pytest.fixture
def pub(batch_repo):
    configure(batch_repo)
    published(batch_repo)
    return batch_repo


def brief(repo):
    done = ok(work(repo, "batch", "brief", "batch-1"))
    path = done.stdout.strip().splitlines()[-1]
    return done, path, open(path).read()


def section(text, heading):
    return text.split("## %s\n" % heading, 1)[1].split("\n## ", 1)[0]


def test_the_first_brief_gives_the_batchs_range_and_no_other_commit(pub):
    text = brief(pub)[2]
    forked = batch_plan.find(pub, "batch-1").forked_from
    head = git(pub, "rev-parse", "batch-1").strip()
    lines = text.splitlines()
    assert lines[:3] == ["# The review of batch-1's pull request", "", "Review: 1 (first; the pull request is unreviewed)"]
    assert "Range: %s..%s" % (forked, head) in lines and "Head: %s" % head in lines
    assert "Findings file: %s" % (scratch(pub) / "findings.md") in lines
    reply = lines[lines.index("Findings file: %s" % (scratch(pub) / "findings.md")) + 1]
    assert reply.startswith("Reply: the findings file's content and nothing else"), reply  # plan 7 review, B1
    want = git(pub, "rev-list", "--reverse", "%s..batch-1" % forked).split()
    listed = [line.split()[1] for line in section(text, "Commits").splitlines() if line.startswith("- ")]
    assert len(listed) == len(want) and all(w.startswith(s) for s, w in zip(listed, want)), (listed, want)
    for subject in git(pub, "log", "--format=%s", "%s..main" % forked).splitlines():
        assert subject.startswith("work batch") and subject not in section(text, "Commits")
    change = (scratch(pub) / "change.diff").read_text()
    assert "src/b1.txt" in change and ".shop/" not in change
    order = ["## Items", "## Judgement decisions", "## Rules", "## Size", "## Runs", "## Commits", "## Change"]
    assert [text.index(h) for h in order] == sorted(text.index(h) for h in order)


def test_the_first_brief_gives_every_requirement_of_its_items(pub):
    items = section(brief(pub)[2], "Items")
    assert '- b1 "Abandon": .shop/backlog/b1.md' in items and "work-queue#r5: %s" % ABANDON in items
    assert '- b2 "Exit": .shop/backlog/b2.md' in items and "work-queue#r6: %s" % SECOND in items


def test_a_parked_item_is_not_in_the_brief(batch_repo):
    configure(batch_repo)
    published(batch_repo, park=True)
    items = section(brief(batch_repo)[2], "Items")
    assert 'b1 "Abandon"' in items and "b2" not in items


def decision(repo, name, tier):
    path = repo / "spec" / "decisions" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('---\nid: design-decision/ex.com/prod/ctx/%s\nsummary: "The %s one."\ntier: %s\n---\n\n# %s\n'
                    % (name[:-3], tier, tier, name))


def test_the_brief_lists_the_judgement_decisions(pub):
    assert "none: no design-decision is tier: judgement" in section(brief(pub)[2], "Judgement decisions")
    decision(pub, "0001-small.md", "judgement")
    decision(pub, "0002-check.md", "check")
    git(pub, "add", "-A")
    git(pub, "commit", "-q", "-m", "decisions")
    listed = section(brief(pub)[2], "Judgement decisions")
    assert "spec/decisions/0001-small.md: The judgement one." in listed and "0002-check" not in listed


def test_the_brief_gives_the_runs_and_the_size(pub):
    text = brief(pub)[2]
    runs = section(text, "Runs")
    assert "python3 -c \"print('ran')\"" in runs and "Exit code: 0" in runs and "    ran" in runs
    size = section(text, "Size")
    assert "files, +" in size and "limit 1000" in size and "over the limit" not in size
    configure(pub, "size = 1\n")
    assert "over the limit" in section(brief(pub)[2], "Size")


def test_brief_leaves_the_checkout_alone(pub):
    before = state(pub)
    _, path, _ = brief(pub)
    assert state(pub) == before
    trees = pub / ".shop" / "worktrees"
    assert path == str(scratch(pub) / "brief.md") and scratch(pub).parent == trees
    assert (scratch(pub) / "change.diff").is_file()


def ahead(repo):
    commit_on(repo, "batch-1", "src/late.txt", "late\n", "late\n\nItem: b1")


def building(repo):
    path = repo / ".shop/batches/1/plan.md"
    path.write_text(path.read_text().replace("status: in-review", "status: building"))
    git(repo, "commit", "-q", "-am", "building again")


def elsewhere(repo):
    git(repo, "checkout", "-q", "-b", "elsewhere")


REFUSED = {"building": (building, "work batch brief: batch-1 is building"),
           "unpushed": (ahead, "work batch review"),
           "branch": (elsewhere, "run it on main")}


@pytest.mark.parametrize("case", sorted(REFUSED))
def test_brief_refuses(pub, case):
    make, named = REFUSED[case]
    make(pub)
    before = state(pub)
    done = work(pub, "batch", "brief", "batch-1")
    assert done.returncode == 1 and named in done.stderr and done.stderr.startswith("work: work batch brief: "), \
        done.stderr
    assert state(pub) == before and not (scratch(pub) / "brief.md").exists()


def test_a_second_brief_starts_fresh(pub):
    brief(pub)
    findings(pub).write_text("old\n")
    done, _, _ = brief(pub)
    assert done.stdout.splitlines()[0] == "removed an old findings.md"
    assert not findings(pub).exists()


def test_a_commit_subject_with_quotes_is_escaped(pub):
    """Review M4: `## Commits` gives each subject in one pair of quotes, a `"` in it escaped."""
    listed = [line for line in section(brief(pub)[2], "Commits").splitlines() if line.startswith("- ")]
    shape = re.compile(r'^- [0-9a-f]{7,} "(?:[^"\\]|\\.)*"(?: Item: [^"]*)?(?: Finding: [^"]*)?$')
    assert all(shape.match(line) for line in listed), listed
    assert any('\\"' in line for line in listed), listed


BASE_CHECK = "import pathlib, sys\nsys.exit(0 if pathlib.Path('src/b1.txt').exists() else 1)\n"


def test_each_run_gives_the_bases_exit_code_once_a_batch(batch_repo):
    """Review S5, Q2: each check is run at `forked_from` too, once a batch, so a failure the batch did not cause is
    told apart from one it did."""
    (batch_repo / "check.py").write_text(BASE_CHECK)
    git(batch_repo, "add", "check.py")
    configure(batch_repo, 'checks = ["python3 check.py"]\n')
    published(batch_repo)
    before = state(batch_repo)
    assert "Exit code: 0 (base: 1)" in section(brief(batch_repo)[2], "Runs")
    assert state(batch_repo) == before
    assert not any(p.name.endswith("-base") for p in (batch_repo / ".shop" / "worktrees").iterdir())
    cache = scratch(batch_repo) / "base-runs.json"
    cache.write_text(cache.read_text().replace(": 1", ": 7"))
    assert "Exit code: 0 (base: 7)" in section(brief(batch_repo)[2], "Runs")
