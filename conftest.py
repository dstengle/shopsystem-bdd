"""`--work-item <name>`: run only the scenarios tagged with a requirement the work-item accepts."""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent


def pytest_addoption(parser):
    parser.addoption("--work-item", default=None, help="run only the scenarios of the requirements it accepts")


def accepted(name):
    for path in (ROOT / ".shop" / "work").glob("*/%s.md" % name):
        found = re.search(r"(?m)^accepts: \[(.*)\]$", path.read_text())
        if found:
            ids = set()
            for one in found.group(1).split(","):
                cap, _, rs = one.strip().partition("#")
                lo, _, hi = rs.lstrip("r").partition("-r")
                for n in range(int(lo), int(hi or lo) + 1):
                    ids.add((cap, "r%d" % n))
            return ids
    raise SystemExit("--work-item %s: no such work-item under .shop/work/" % name)


def pytest_collection_modifyitems(config, items):
    name = config.getoption("--work-item")
    if not name:
        return
    want = accepted(name)
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
