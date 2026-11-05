"""`measure show` and `measure compare` of batches (telemetry r4; workflow simplification plan 7, D12): a batch name
resolved to its newest measurement, two batches side by side with their ratio, an unmeasured batch and a batch set
against an initiative refused, and an initiative's records compared as before."""
import subprocess
import sys

import measure_batch_show
from backlog_testing import SCRIPTS
from measure_batch_testing import FIGURES, write_measurement

M1 = ('{"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14, '
      '"round_trips": 7}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14, "round_trips": 7}}')
M3 = ('{"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", '
      '"started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": '
      '80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}')
# what `measure compare m1.md m3.md` printed at 9d765bb8, batch-measurement r21's two records
BEFORE = """\
total             | a  | b | ratio
------------------+----+---+------
stages            | 1  | 0 | 0
sessions          | 1  | 0 | 0
turns             | 14 |   | -
round trips       | 7  |   | -
output tokens     |    |   | -
new input tokens  |    |   | -
cache-read tokens |    |   | -
cost              |    |   | -
time              |    |   | -

total       | a | b | ratio
------------+---+---+------
round trips | 0 | 6 | -
tool uses   | 0 | 2 | -
compactions | 0 | 1 | -
"""


def measure(repo, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / "measure"), *args], cwd=repo, capture_output=True,
                          text=True, timeout=60)


def batch(name, cost):
    return dict(FIGURES, batch=name, cost=cost)


def lines(text):
    return {line.split("|")[0].strip(): [c.strip() for c in line.split("|")[1:]] for line in text.splitlines()
            if "|" in line}


def test_compare_by_batch_name(backlog_repo):
    write_measurement(backlog_repo, "2026-11-01", batch("batch-2", 1.0))
    write_measurement(backlog_repo, "2026-11-02", batch("batch-3", 2.5))
    done = measure(backlog_repo, "compare", "batch-2", "batch-3")
    assert done.returncode == 0, done.stderr
    assert [c.strip() for c in done.stdout.splitlines()[0].split("|")] == ["total", "batch-2", "batch-3", "ratio"]
    rows = lines(done.stdout)
    for name in ("wall time", "cost", "planning cost", "review cost", "defects per item"):
        assert name in rows, (name, done.stdout)
    assert rows["cost"] == ["1.00", "2.50", "2.5"]


def test_a_batch_name_takes_its_newest_measurement(backlog_repo):
    """Review Focus 5."""
    write_measurement(backlog_repo, "2026-11-01", batch("batch-2", 1.0))
    newest = write_measurement(backlog_repo, "2026-11-03", batch("batch-2", 3.0))
    assert measure_batch_show.resolve(backlog_repo, "batch-2") == newest
    done = measure(backlog_repo, "compare", "batch-2", "batch-2")
    assert done.returncode == 0, done.stderr
    assert lines(done.stdout)["cost"] == ["3.00", "3.00", "1"]


def test_an_unmeasured_batch_is_refused(backlog_repo):
    """Review Focus 5."""
    write_measurement(backlog_repo, "2026-11-01", batch("batch-2", 1.0))
    done = measure(backlog_repo, "compare", "batch-2", "batch-7")
    assert done.returncode == 1, done.stdout
    assert "batch-7" in done.stderr and "measure batch batch-7" in done.stderr, done.stderr


def test_a_batch_and_an_initiative_do_not_compare(backlog_repo):
    """Review Focus 5."""
    write_measurement(backlog_repo, "2026-11-01", batch("batch-2", 1.0))
    (backlog_repo / "m1.md").write_text("# m1\n\n```json\n%s\n```\n" % M1)
    done = measure(backlog_repo, "compare", "batch-2", "m1.md")
    assert done.returncode == 1, done.stdout
    assert "is a batch's measurement and" in done.stderr, done.stderr


def test_show_prints_a_batch(backlog_repo):
    path = write_measurement(backlog_repo, "2026-11-01", FIGURES)
    done = measure(backlog_repo, "show", str(path))
    assert done.returncode == 0, done.stderr
    for words in ("cost by role", "sessions", "review findings by grade", "shopsystem-bdd:pr-reviewer"):
        assert words in done.stdout, (words, done.stdout)
    assert any(r[:2] == ["shopsystem-bdd:pr-reviewer", "review"] for r in lines(done.stdout).values() if len(r) > 2)


def test_an_initiatives_records_compare_as_before(tmp_path):
    for name, text in (("m1.md", M1), ("m3.md", M3)):
        (tmp_path / name).write_text("# %s\n\n```json\n%s\n```\n" % (name, text))
    done = measure(tmp_path, "compare", "m1.md", "m3.md")
    assert done.returncode == 0, done.stderr
    assert done.stdout == BEFORE
