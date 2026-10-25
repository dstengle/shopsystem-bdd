"""The plugin's pytest plugin: `--work-item <name>` runs the scenarios tagged with a requirement the work-item
accepts, deselects the other scenarios and keeps every test that is not a scenario (a probe, a script's test). It
refuses, saying so, a run that collects scenarios and none the work-item accepts, unless every requirement it accepts
is of a guarantees capability (spec/capabilities/<cap>.md with `group: guarantees` in its frontmatter): then it
deselects them all, and a run left with no test exits 0. `work run` loads it with
`-p work_items`, the scripts directory on PYTHONPATH, so a repository it delivers needs nothing of its own for the
option; this repository's conftest.py loads it the same way.

A work-item is .shop/work/<initiative>/<name>.md, found in the nearest directory at or above where pytest was started
that has .shop/work/; its `accepts: [<capability>#r<n>, <capability>#r<n>-r<m>, ...]` names the requirements. A
scenario is pytest-bdd's, its capability the stem of its feature file and its requirements its `@r<n>` tags.

With `--whole-suite` too, every test runs (the whole suite before the work-item's merge), and a scenario whose
requirement a work-item other than the work-item, neither green nor withdrawn, accepts, or a capability-proposal
neither formulated nor withdrawn adds or changes, is expected to fail: an xfail (supervision r43, r122). Standard library and pytest only.
"""
import pathlib
import re

import pytest


def pytest_addoption(parser):
    parser.addoption("--work-item", default=None, help="run only the scenarios of the requirements it accepts")
    parser.addoption("--whole-suite", action="store_true", default=False,
                     help="with --work-item, run every test: the whole suite before the work-item's merge")


def work_dir(start):
    """The .shop/work/ of the nearest directory at or above `start` that has one; else None."""
    for here in (start, *start.parents):
        if (here / ".shop" / "work").is_dir():
            return here / ".shop" / "work"
    return None


def requirements(text):
    """The (capability, requirement) pairs a work-item's text `accepts`."""
    found = re.search(r"(?m)^accepts: \[(.*)\]$", text)
    ids = set()
    for one in found.group(1).split(",") if found else []:
        cap, _, rs = one.strip().strip("'\"").partition("#")
        lo, _, hi = rs.lstrip("r").partition("-r")
        if lo.isdigit() and (hi or lo).isdigit():
            ids.update((cap, "r%d" % n) for n in range(int(lo), int(hi or lo) + 1))
    return ids


def accepted(name, start):
    """The (capability, requirement) pairs work-item `name` accepts; a work-item that is not there is refused."""
    work = work_dir(pathlib.Path(start).resolve())
    for path in sorted(work.glob("*/%s.md" % name)) if work else []:
        if re.search(r"(?m)^accepts: \[(.*)\]$", path.read_text()):
            return requirements(path.read_text())
    raise SystemExit("--work-item %s: no such work-item under .shop/work/" % name)


def acceptors(start):
    """{(capability, requirement): {(work-item, status), ...}} of every work-item under .shop/work/."""
    work = work_dir(pathlib.Path(start).resolve())
    found = {}
    for path in sorted(work.glob("*/*.md")) if work else []:
        text = path.read_text()
        if re.search(r"(?m)^kind: work-item$", text):
            status = re.search(r"(?m)^status: (\S+)$", text)
            for req in requirements(text):
                found.setdefault(req, set()).add((path.stem, status.group(1) if status else None))
    return found


def proposals(start):
    """{(capability, requirement): {proposal, ...}} that a capability-proposal under .shop/work/, neither formulated
    nor withdrawn, adds or changes (supervision r122)."""
    work = work_dir(pathlib.Path(start).resolve())
    found = {}
    for path in sorted(work.glob("*/*.md")) if work else []:
        text = path.read_text()
        status = re.search(r"(?m)^status: (\S+)$", text)
        if re.search(r"(?m)^kind: capability-proposal$", text) and (status.group(1) if status else None) not in (
                "formulated", "withdrawn"):
            for field in ("adds", "changes"):
                line = re.search(r"(?m)^%s: \[(.*)\]$" % field, text)
                for req in requirements("accepts: [%s]" % line.group(1) if line else ""):
                    found.setdefault(req, set()).add(path.stem)
    return found


def scenario_of(item):
    """The pytest-bdd scenario `item` runs, as (capability, its requirement tags); None for any other test."""
    scenario = getattr(getattr(item, "function", None), "__scenario__", None)
    if scenario is None:
        return None
    return pathlib.Path(scenario.feature.filename).stem, scenario.tags


def expect_red(config, items, name):
    """Mark as xfail each scenario whose requirement a work-item other than `name`, neither green nor withdrawn,
    accepts."""
    by = acceptors(config.invocation_params.dir)
    drafts = proposals(config.invocation_params.dir)
    for item in items:
        found = scenario_of(item)
        if found is None:
            continue
        who = set().union(*[by.get((found[0], tag), set()) for tag in found[1]])
        open_ = sorted(other for other, status in who if other != name and status not in ("green", "withdrawn"))
        open_ += sorted(set().union(*[drafts.get((found[0], tag), set()) for tag in found[1]]))
        if open_:
            item.add_marker(pytest.mark.xfail(reason="expected: accepted by %s, neither green nor withdrawn"
                                              % ", ".join(open_), strict=False))


def pytest_collection_modifyitems(config, items):
    name = config.getoption("--work-item")
    if not name:
        return
    if config.getoption("--whole-suite"):
        expect_red(config, items, name)
        return
    want = accepted(name, config.invocation_params.dir)
    keep, scenarios = [], 0
    for item in items:
        found = scenario_of(item)
        scenarios += found is not None
        if found is None or any((found[0], tag) in want for tag in found[1]):
            keep.append(item)
    if scenarios and len(keep) == len(items) - scenarios and not all(guarantees(config, c) for c, _ in want):
        raise SystemExit("--work-item %s: %s accepts none of the scenarios it collected" % (name, name))
    config.hook.pytest_deselected(items=[i for i in items if i not in keep])
    items[:] = keep


def guarantees(config, cap):
    """Whether spec/capabilities/<cap>.md, beside the .shop/ of the work-items, has `group: guarantees` in its
    frontmatter."""
    work = work_dir(pathlib.Path(config.invocation_params.dir).resolve())
    path = (work.parent.parent if work else pathlib.Path(config.rootpath)) / "spec" / "capabilities" / ("%s.md" % cap)
    head = path.read_text().split("---\n")[1:2] if path.is_file() else []
    return bool(head) and re.search(r"(?m)^group: guarantees$", head[0]) is not None


def pytest_sessionfinish(session, exitstatus):
    """A work-item all of whose requirements are of guarantees capabilities, left with no test, succeeds. Decided
    from the work-item and the spec, so on the xdist controller as on a worker."""
    config = session.config
    name = config.getoption("--work-item")
    if exitstatus != pytest.ExitCode.NO_TESTS_COLLECTED or not name or config.getoption("--whole-suite"):
        return
    if all(guarantees(config, c) for c, _ in accepted(name, config.invocation_params.dir)):
        session.exitstatus = pytest.ExitCode.OK
