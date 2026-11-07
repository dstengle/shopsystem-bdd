"""migration-tools' condition Givens (design-r2 §4.3: primitive conditions): `a repository r1` is the scenario's own
repository, and `the repository r1 is <condition>` checks that the files the scenario's example data holds give the
repository that condition, by the condition's gloss in spec/capabilities/migration-tools.md (CHECKS below), so a
scenario cannot claim a condition its files do not show. `an untracked file u1` writes `u1.md`, never committed; the
error that names it is read by migration_tools_handlers' `exits_err`."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

from vocab import handler

from scenarios.migration_old import number, plugin

OLD = ("decisions/", "work/", "records/", "docs/superpowers/", "adrs/")
VERSION = re.compile(r"\d+\.\d+\.\d+")


def files(step):
    return step.context.get("tracked", {})


def ledger(step):
    return files(step).get("spec/decisions.md", "")


def version(step):
    """What `.shop/plugin-version` holds, stripped; None when the repository has none."""
    text = files(step).get(".shop/plugin-version")
    return None if text is None else text.strip()


def release(step):
    held = version(step)
    return number(held) if held and VERSION.fullmatch(held) else None


def initiatives(step):
    return [t for rel, t in files(step).items() if re.fullmatch(r"\.shop/work/[^/]+/initiative\.md", rel)]


def is_open(text):
    return not re.search(r"^status: (done|abandoned)$", text, re.MULTILINE)


def current(step):
    return release(step) == number(plugin()[1])


def idless(step):
    return any(rel.startswith("spec/capabilities/") and re.search(r"^- \*\*", text, re.MULTILINE)
               for rel, text in files(step).items())


def conflicting(step):
    entries = re.findall(r"^## decision/(\S+)$", ledger(step), re.MULTILINE)
    return any("decisions/%s.md" % name in files(step) for name in entries)


def uncodified(step):
    return release(step) == (0, 29, 0) and any(
        rel.startswith("spec/capabilities/") and "language: codified-1" not in text for rel, text in files(step).items())


CHECKS = {
    "unmigrated": lambda step: any(rel.startswith(OLD) for rel in files(step)),
    "ledgered": lambda step: bool(ledger(step)),
    "superseding": lambda step: "\nsupersedes: " in ledger(step),
    "qualified": lambda step: bool(re.search(r"^supersedes: \S+ \(", ledger(step), re.MULTILINE)),
    "numberless": lambda step: bool(re.search(r"^## decision/[^\d\s]", ledger(step), re.MULTILINE)),
    "idless": idless,
    "conflicting": conflicting,
    "unversioned": lambda step: version(step) is None and any(rel.startswith(".shop/") for rel in files(step)),
    "misversioned": lambda step: version(step) is not None and release(step) is None,
    "behind": lambda step: release(step) == (0, 23, 1),
    "outdated": lambda step: release(step) == (0, 24, 0),
    "uncodified": uncodified,
    "queued": lambda step: release(step) == (1, 0, 0),
    "unframed": lambda step: release(step) is not None and (1, 0, 0) < release(step) < (3, 0, 0),
    "current": current,
    "ahead": lambda step: release(step) is not None and release(step) > number(plugin()[1]),
    "idle": lambda step: current(step) and not any(is_open(t) for t in initiatives(step)),
    "busy": lambda step: any(is_open(t) for t in initiatives(step)),
    "shopless": lambda step: not any(rel.startswith(".shop/") for rel in files(step)),
}


@handler("GivenK", "repository")
def repository(step):
    step.context.setdefault("tracked", {})


@handler("GivenK_C", "repository")
def repository_is(step):
    word = step.text.rsplit(" is ", 1)[1]
    assert CHECKS[word](step), "the scenario's files do not make the repository %s: %s" % (word, sorted(files(step)))


@handler("GivenK", "untracked file")
def untracked(step):
    rel = "%s.md" % step.names[0]
    step.context.setdefault("untracked", {})[rel] = "not committed\n"
    step.context.setdefault("says", {})[step.names[0]] = rel


@handler("GivenK_C", "untracked file")
def untracked_is(step):
    assert step.text.endswith(" is uncommitted"), step.text
    assert step.context["says"][step.names[0]] in step.context["untracked"]
