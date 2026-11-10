"""batch-measurement's handlers (b240, phase 19: the capability in grammar 4): a measurement's example rows written by
its Given (`the measurement `m1` holds:`), every `measure ...` command of the generated feature run as `measure`'s
main in-process on the World's day (batch_measurement_world.py), and the Thens reading what it printed.

The scenario's instances (`the measurement m1`, `the stage row s1` ...) are its lines' things; their example data is
the given block, so a measurement instance is the given block's measurement of its rank (the scenario's first
measurement the first written), and the rows a Then names are read off that measurement's figures. `measure compare`
on one measurement compares it with itself; on two, each When adds its measurement and runs the comparison again."""
import json
import pathlib
import re
import shlex
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

from vocab import handler

from scenarios import batch_measurement_world as bw


def _queue_world():
    """work_queue_world as the other handler modules load it (its `local` table is that copy's)."""
    import importlib.util
    if "shop_work_queue_world" not in sys.modules:
        spec = importlib.util.spec_from_file_location("shop_work_queue_world", HERE / "work_queue_world.py")
        sys.modules["shop_work_queue_world"] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules["shop_work_queue_world"]


local = _queue_world().local

FEATURE = HERE.parents[1] / "features" / "batch-measurement.feature"
KINDS = ("measurement", "stage row", "round trip", "session row", "tool use", "dispatch", "compaction", "total row")


def bare(word):
    return word.strip("`")


def world(step):
    if "world" not in step.context:
        step.context["world"] = bw.World(step.repo)
    return step.context["world"]


def ours(step):
    return "measurements" in step.context


# --- Givens ---


@handler("GivenCodeText", "measurement")
def given_measurement(step):
    name = bare(step.names[0])
    path = step.repo / ("%s.md" % name)
    path.write_text("# Measurement\n\n```json\n%s\n```\n" % step.docstring)
    step.context.setdefault("measurements", []).append(name)


def instance(step):
    """`a measurement m1`, `a stage row s1` ...: the example data holds them; a measurement takes its rank."""
    if not ours(step):
        return False
    if step.kind == "measurement":
        named = step.context.setdefault("named", {})
        named.setdefault(step.names[0], step.context["measurements"][min(len(named), len(step.context["measurements"]) - 1)])
    return None


for _kind in KINDS:
    local("GivenK", _kind)(instance)
for _kind in ("measurement", "stage row", "round trip", "session row", "tool use"):
    handler("GivenK", _kind)(lambda step: None)


def code_of(step, name):
    """The given block's measurement the scenario's measurement `name` is: its rank, else the first."""
    named = step.context.setdefault("named", {})
    given = step.context["measurements"]
    return named.setdefault(name, given[min(len(named), len(given) - 1)])


# --- the When ---


def runs_measure(step):
    w = world(step)
    command = shlex.split(bare(step.command))[1:]
    files = step.context.setdefault("on", [])
    files += ["%s.md" % code_of(step, n) for n in step.names]
    if command == ["compare"] and len(files) == 1:
        files = files * 2
    w.run(step.fixtures("monkeypatch"), step.fixtures("capsys"), *command, *files)


for _command in sorted(set(re.findall(r"When the person runs (`measure[^`]*`)", FEATURE.read_text()))):
    handler("WhenRuns", _command)(runs_measure)


# --- Thens ---


def figures(step):
    """The figures of each measurement the command ran on."""
    return [json.loads((step.repo / f).read_text().split("```json\n", 1)[1].split("\n```", 1)[0])
            for f in step.context["on"]]


def shown(step, np):
    """The words `measure` prints for the thing a noun phrase names, read off the measurements' figures."""
    sessions = [s for m in figures(step) for s in m.get("sessions", [])]
    if np.startswith("the number of round trips"):
        return ["round trips"] + [str(s["round_trips"]) for m in figures(step) for s in m["stages"]]
    if np.startswith("the number of tool uses in"):
        return ["tool uses", str(sum(n for s in sessions for n in s["tool_uses"].values()))]
    if np.startswith("the number of tool uses"):
        return ["tool uses"] + ["%s %d" % kv for s in sessions for kv in s["tool_uses"].items()]
    if np.startswith("the number of compactions"):
        return ["compactions"] + [str(s["compactions"]) for s in sessions]
    if np.startswith("the stage row"):
        return ["stages"] + [s["work-item"] for m in figures(step) for s in m["stages"]]
    if np.startswith("the dispatch"):
        return ["dispatched"] + [d for s in sessions for d in s["dispatched"]]
    if np.startswith("the total row"):
        return ["total"]
    if np.startswith("the ratio"):
        return ["ratio"]
    raise AssertionError("no reading of %r" % np)


@handler("ThenPrints", "`measure`")
def prints(step):
    w = world(step)
    assert w.code == 0, w.err
    for np in step.nps:
        for word in shown(step, np):
            assert word in w.out, (np, word, w.out)


@handler("ThenPrintsNot", "`measure`")
def prints_not(step):
    w = world(step)
    assert w.code == 0, w.err
    for np in step.nps:
        word = {"a round trip": "round trips"}[np]
        assert word not in w.out, (np, w.out)


@local("ThenDoes")
def has(step):
    """`the measurement m1 has the total row t1`: the measurement `measure` read gives one."""
    if not ours(step) or step.term != "has":
        return False
    assert world(step).code == 0, world(step).err
    assert all("totals" in m for m in figures(step)), step.text
    return None
