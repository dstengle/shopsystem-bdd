"""The tiers of spec/decisions/ (decision-tiers): a decision's `tier`, its `enforced_by` entries told apart into tests
and requirements, and `model decisions --check`'s runs of each `check` decision's tests (plan 6, D2, D5): one pytest
run a decision, in the repository, under the project's interpreter, with the repository's `addopts` cleared and
nothing of its own written; a run holds when pytest exits 0 having passed a test and skipped, xfailed, xpassed or
deselected none (review S1). Standard library only."""

import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from model_parse import as_list, decision_files, frontmatter
from tools_env import project_python

TIERS = ("check", "requirement", "judgement")
ROUTES = ("scenario", "check", "judgement", "monitor")     # a decision's verification routes (verified_by, b129)
TIMEOUT = 600       # seconds a decision's run may take
WORKERS = 4         # decisions run side by side
TAIL = 20           # lines of pytest's output a failing decision shows
REQUIREMENT = re.compile(r"^[\w.-]+(?:/[\w.-]+)*#r\d+(?:-r\d+)?(?:@0\.29)?$")   # `<capability>#r<n>`, `#r<a>-r<b>`
NOT_RUN = ("skipped", "xfailed", "xpassed", "deselected")    # outcomes of a test that enforces nothing
HISTORY = ("superseded", "rejected")


def split(entries):
    """(tests, requirements): an entry in the form of a requirement id (`<capability>#r<n>` or `#r<a>-r<b>`) is a
    requirement, any other a pytest node id (review M3: a parametrised id may hold `#`)."""
    tests, requirements = [], []
    for entry in entries:
        entry = str(entry).strip()
        (requirements if REQUIREMENT.match(entry) else tests).append(entry)
    return tests, requirements


def test_file(entry):
    """The file of a pytest node id: the part before the first `::`."""
    return str(entry).split("::", 1)[0]


def wrong(root, tier, tests, requirements):
    """The file problems of a decision's tier and entries (D2): a tier outside the three, an entry of the wrong kind for
    its tier, `enforced_by` on a judgement decision, a test whose file is not under the root."""
    out = []
    if tier is not None and tier not in TIERS:
        out.append(f"tier {tier!r} is not one of {', '.join(TIERS)}")
    if tier == "judgement" and (tests or requirements):
        out.append("a judgement decision gives no enforced_by")
        return out
    for t in tests:
        if tier == "requirement":
            out.append(f"enforced_by {t}: a test, on a requirement decision")
        elif not of_repository(root, t):
            out.append(f"enforced_by {t}: not a file of this repository")
    out += [f"enforced_by {q}: a requirement, on a check decision" for q in requirements if tier == "check"]
    return out


def of_repository(root, entry):
    """Whether a pytest node id names a file under the root: not an option, not a path out of it (review S2)."""
    path = (Path(root) / test_file(entry)).resolve()
    return not entry.startswith("-") and path.is_file() and path.is_relative_to(Path(root).resolve())


@dataclass
class Decision:
    rel: str
    ident: str
    status: str | None
    tier: str | None
    tests: list[str]
    requirements: list[str]
    summary: str

    @property
    def runs(self):
        """A `check` decision in force: history's tests are never run (review M2)."""
        return self.tier == "check" and self.status not in HISTORY


def decisions(root):
    """Every decision file with an id, in file order."""
    out = []
    for path in decision_files(root):
        data, _ = frontmatter(path.read_text())
        if data.get("id"):
            tests, reqs = split(as_list(data.get("enforced_by")))
            out.append(Decision(path.relative_to(root).as_posix(), data["id"], data.get("status"), data.get("tier"),
                                tests, reqs, str(data.get("summary") or "")))
    return out


@dataclass
class Ran:
    decision: Decision
    code: int | None       # None: timed out, not run, or no test to run
    tail: str
    timeout: int | None = None
    refused: str | None = None     # why a run that exits 0, or is never started, does not hold

    @property
    def holds(self):
        return self.code == 0 and self.refused is None

    @property
    def why(self):
        if self.refused:
            return self.refused
        return f"timed out after {self.timeout} s" if self.code is None else f"exit {self.code}"


def run(root, decision, timeout=TIMEOUT):
    """The decision's tests, run alone under the project's interpreter: no bytecode, no cache, the repository's addopts
    cleared; an entry that is not a test of the repository is not run."""
    if not decision.tests:
        return Ran(decision, None, "names no test")
    bad = [t for t in decision.tests if not of_repository(root, t)]
    if bad:
        return Ran(decision, None, "", refused=f"not a test of this repository: {bad[0]}")
    env = {k: v for k, v in os.environ.items() if k != "PYTEST_ADDOPTS"}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cmd = [project_python(str(root))[0], "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "addopts=", *decision.tests]
    try:
        done = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        return Ran(decision, None, tail(out), timeout)
    return Ran(decision, done.returncode, tail(done.stdout + done.stderr), refused=unrun(done))


def unrun(done):
    """Why a run that exits 0 enforces nothing, from pytest's summary line: a test skipped, xfailed, xpassed or
    deselected, or none passed (review S1); None when it holds or when its exit already fails it."""
    if done.returncode:
        return None
    lines = done.stdout.rstrip().splitlines()
    counts = {word: int(n) for n, word in re.findall(r"(\d+) (\w+)", lines[-1] if lines else "")}
    found = [f"{counts[w]} {w}" for w in NOT_RUN if counts.get(w)]
    if found:
        return "not run: " + ", ".join(found)
    return None if counts.get("passed") else "nothing passed"


def tail(text):
    return "\n".join(text.rstrip().splitlines()[-TAIL:])


def check_tests(root, timeout=TIMEOUT):
    """Every `check` decision's run, WORKERS at a time, in file order."""
    root = Path(root)
    found = [d for d in decisions(root) if d.runs]
    with ThreadPoolExecutor(WORKERS) as pool:
        return list(pool.map(lambda d: run(root, d, timeout), found))


def report(ran):
    """The lines `model decisions --check` prints for the runs, and whether every decision holds."""
    lines = []
    for r in ran:
        head = f"{r.decision.rel} ({r.decision.ident}): "
        if r.holds:
            lines.append(f"holds    {head}{', '.join(r.decision.tests)}")
            continue
        if not r.decision.tests:
            lines.append(f"failing  {head}names no test")
            continue
        lines.append(f"failing  {head}{', '.join(r.decision.tests)}: {r.why}")
        lines += ["    " + line for line in r.tail.splitlines()]
    held = sum(r.holds for r in ran)
    lines.append(f"{len(ran)} check decisions: {held} hold, {len(ran) - held} failing")
    return lines, held == len(ran)
