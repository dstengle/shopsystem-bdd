"""The plugin's pytest plugin: `--work-item <name>` runs only the scenarios tagged with a requirement the work-item
accepts. `work run` loads it with `-p work_items`, the scripts directory on PYTHONPATH, so a repository it delivers needs
nothing of its own for the option; this repository's conftest.py loads it the same way.

A work-item is .shop/work/<initiative>/<name>.md, found in the nearest directory at or above where pytest was started
that has .shop/work/; its `accepts: [<capability>#r<n>, <capability>#r<n>-r<m>, ...]` names the requirements. A
scenario is pytest-bdd's, its capability the stem of its feature file and its requirements its `@r<n>` tags.
Standard library and pytest only.
"""
import pathlib
import re


def pytest_addoption(parser):
    parser.addoption("--work-item", default=None, help="run only the scenarios of the requirements it accepts")


def work_dir(start):
    """The .shop/work/ of the nearest directory at or above `start` that has one; else None."""
    for here in (start, *start.parents):
        if (here / ".shop" / "work").is_dir():
            return here / ".shop" / "work"
    return None


def accepted(name, start):
    """The (capability, requirement) pairs work-item `name` accepts; a work-item that is not there is refused."""
    work = work_dir(pathlib.Path(start).resolve())
    for path in sorted(work.glob("*/%s.md" % name)) if work else []:
        found = re.search(r"(?m)^accepts: \[(.*)\]$", path.read_text())
        if found:
            ids = set()
            for one in found.group(1).split(","):
                cap, _, rs = one.strip().strip("'\"").partition("#")
                lo, _, hi = rs.lstrip("r").partition("-r")
                for n in range(int(lo), int(hi or lo) + 1):
                    ids.add((cap, "r%d" % n))
            return ids
    raise SystemExit("--work-item %s: no such work-item under .shop/work/" % name)


def pytest_collection_modifyitems(config, items):
    name = config.getoption("--work-item")
    if not name:
        return
    want = accepted(name, config.invocation_params.dir)
    keep = []
    for item in items:
        scenario = getattr(getattr(item, "function", None), "__scenario__", None)
        if scenario is None:
            continue
        cap = pathlib.Path(scenario.feature.filename).stem
        if any((cap, tag) in want for tag in scenario.tags):
            keep.append(item)
    if not keep:
        raise SystemExit("--work-item %s: no scenario carries a requirement it accepts" % name)
    config.hook.pytest_deselected(items=[i for i in items if i not in keep])
    items[:] = keep
