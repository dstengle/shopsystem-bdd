"""The tiers of spec/decisions/ (decision-tiers): a decision's `tier`, its `enforced_by` entries told apart into tests
and requirements, and `model decisions --check`'s runs of each `check` decision's tests (plan 6, D2, D5): one pytest
run a decision, in the repository, with the repository's `addopts` cleared and nothing written. Standard library
only."""

import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from model_parse import as_list, decision_files, frontmatter

TIERS = ("check", "requirement", "judgement")
TIMEOUT = 600       # seconds a decision's run may take
WORKERS = 4         # decisions run side by side
TAIL = 20           # lines of pytest's output a failing decision shows


def split(entries):
    """(tests, requirements): an entry holding `#` is a requirement id, any other a pytest node id."""
    tests, requirements = [], []
    for entry in entries:
        (requirements if "#" in str(entry) else tests).append(str(entry).strip())
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
        elif not (root / test_file(t)).is_file():
            out.append(f"enforced_by {t}: not a file of this repository")
    out += [f"enforced_by {q}: a requirement, on a check decision" for q in requirements if tier == "check"]
    return out


@dataclass
class Decision:
    rel: str
    ident: str
    status: str | None
    tier: str | None
    tests: list[str]
    requirements: list[str]
    summary: str


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
    code: int | None       # None: timed out, or no test to run
    tail: str
    timeout: int | None = None

    @property
    def holds(self):
        return self.code == 0


def run(root, decision, timeout=TIMEOUT):
    """The decision's tests, run alone: no bytecode, no cache, the repository's addopts cleared."""
    if not decision.tests:
        return Ran(decision, None, "names no test")
    env = {k: v for k, v in os.environ.items() if k != "PYTEST_ADDOPTS"}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cmd = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "addopts=", *decision.tests]
    try:
        done = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        return Ran(decision, None, tail(out), timeout)
    return Ran(decision, done.returncode, tail(done.stdout + done.stderr))


def tail(text):
    return "\n".join(text.rstrip().splitlines()[-TAIL:])


def check_tests(root, timeout=TIMEOUT):
    """Every `check` decision's run, WORKERS at a time, in file order."""
    root = Path(root)
    found = [d for d in decisions(root) if d.tier == "check"]
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
        why = f"timed out after {r.timeout} s" if r.code is None else f"exit {r.code}"
        lines.append(f"failing  {head}{', '.join(r.decision.tests)}: {why}")
        lines += ["    " + line for line in r.tail.splitlines()]
    held = sum(r.holds for r in ran)
    lines.append(f"{len(ran)} check decisions: {held} hold, {len(ran) - held} failing")
    return lines, held == len(ran)
