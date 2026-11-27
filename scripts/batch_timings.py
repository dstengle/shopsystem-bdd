"""The durations of a batch's test runs and of its opening (b73, b876, measurement r13): each test run of `work batch
done` and `work batch review` (`timed`), the time `work batch start` took to open the batch (`kept` of `opening`) and
each phase of that opening (`kept` of `phase`, its name the line's `phase`: plumbing.phases' stopwatch), one
JSON line each in `<git common dir>/shopsystem-bdd/timings.jsonl`, shared by the worktrees and never committed; read
back for `measure batch` (`of`, `figures`). A line that cannot be written is left out, never failing the command.
Standard library only."""
import contextlib
import datetime
import json
import time

from batch_git import common_dir

FILE = "shopsystem-bdd/timings.jsonl"
KINDS = ("done", "review", "opening", "phase")


def path(root):
    return common_dir(root) / FILE


def kept(root, batch, kind, seconds, task=None, passed=True, phase=None):
    """One duration of the batch `batch` appended, of an opening phase `phase` when it is of kind `phase`; an OSError
    (a read-only git dir) leaves it out."""
    entry = {"batch": batch, "kind": kind, "task": task, "passed": passed, "seconds": round(seconds, 3),
             "at": datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")}
    if phase is not None:
        entry["phase"] = phase
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


def kept_phases(root, batch, seconds):
    """Each phase {name: seconds} of the opening of `batch` kept as a line of kind `phase`."""
    for name, took in seconds.items():
        kept(root, batch, "phase", took, phase=name)


def _phases(entries):
    """[{phase, seconds}] of the last opening: the phase lines after the opening before it, a name kept again summed."""
    last = [k for k, e in enumerate(entries) if e["kind"] == "opening"]
    since = last[-2] + 1 if len(last) > 1 else 0
    out = {}
    for e in entries[since:]:
        if e["kind"] == "phase" and isinstance(e.get("phase"), str):
            out[e["phase"]] = out.get(e["phase"], 0) + (e.get("seconds") or 0)
    return [{"phase": name, "seconds": round(took)} for name, took in out.items()]


def figures(root, batch):
    """`test_runs` (each done and review run with its seconds), `test_time_seconds` (their sum),
    `opening_time_seconds` (the last opening's, None when none was kept) and `opening_phases` (each phase of the last
    opening with its seconds, in the order kept)."""
    entries = of(root, batch)
    runs = [{k: e.get(k) for k in ("kind", "task", "passed", "at", "seconds")} for e in entries
            if e["kind"] in ("done", "review")]
    openings = [e["seconds"] for e in entries if e["kind"] == "opening"]
    return {"test_runs": runs, "test_time_seconds": round(sum(r["seconds"] or 0 for r in runs)),
            "opening_time_seconds": round(openings[-1]) if openings else None, "opening_phases": _phases(entries)}
