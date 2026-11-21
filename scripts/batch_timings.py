"""The durations of a batch's test runs and of its opening (b73, measurement r12): each test run of `work batch done`
and `work batch review` (`timed`) and the time `work batch start` took to open the batch (`kept` of `opening`), one
JSON line each in `<git common dir>/shopsystem-bdd/timings.jsonl`, shared by the worktrees and never committed; read
back for `measure batch` (`of`, `figures`). A line that cannot be written is left out, never failing the command.
Standard library only."""
import contextlib
import datetime
import json
import time

from batch_git import common_dir

FILE = "shopsystem-bdd/timings.jsonl"
KINDS = ("done", "review", "opening")


def path(root):
    return common_dir(root) / FILE


def kept(root, batch, kind, seconds, task=None, passed=True):
    """One duration of the batch `batch` appended; an OSError (a read-only git dir) leaves it out."""
    entry = {"batch": batch, "kind": kind, "task": task, "passed": passed, "seconds": round(seconds, 3),
             "at": datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")}
    try:
        where = path(root)
        where.parent.mkdir(parents=True, exist_ok=True)
        with open(where, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")
    except OSError:
        pass


@contextlib.contextmanager
def timed(root, batch, kind, task=None):
    """The block's duration kept as a test run of `kind`, refused or not: a failing run took its time too."""
    began, passed = time.monotonic(), False
    try:
        yield
        passed = True
    finally:
        kept(root, batch, kind, time.monotonic() - began, task, passed)


def of(root, batch):
    """The entries of the batch `batch`, in the order kept; a line that does not read is passed over."""
    try:
        text = path(root).read_text(encoding="utf-8")
    except OSError:
        return []
    found = []
    for line in text.splitlines():
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if isinstance(entry, dict) and entry.get("batch") == batch and entry.get("kind") in KINDS:
            found.append(entry)
    return found


def figures(root, batch):
    """`test_runs` (each done and review run with its seconds), `test_time_seconds` (their sum) and
    `opening_time_seconds` (the last opening's, None when none was kept)."""
    entries = of(root, batch)
    runs = [{k: e.get(k) for k in ("kind", "task", "passed", "at", "seconds")} for e in entries
            if e["kind"] != "opening"]
    openings = [e["seconds"] for e in entries if e["kind"] == "opening"]
    return {"test_runs": runs, "test_time_seconds": round(sum(r["seconds"] or 0 for r in runs)),
            "opening_time_seconds": round(openings[-1]) if openings else None}
