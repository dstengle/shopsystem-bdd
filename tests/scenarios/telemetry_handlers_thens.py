"""The Thens of features/telemetry.feature in grammar 4 (b240, phase 19), read off the `Ran` telemetry_handlers'
When leaves: what `measure batch` wrote (its record and figures), the defect `measure defect` wrote, and what
`measure compare` printed. Each is a `local` of work_queue_world's table, which returns False outside telemetry."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

from vocab import handler  # noqa: F401  (the registry loads this module beside the handlers)


def _modules():
    """telemetry_handlers' worlds, loaded under the names the other handler modules give them."""
    import importlib.util
    out = []
    for name, file in (("shop_work_queue_world", "work_queue_world.py"), ("shop_backlog_world", "backlog_world.py"),
                       ("shop_batches_world", "batches_world.py")):
        if name not in sys.modules:
            spec = importlib.util.spec_from_file_location(name, HERE / file)
            sys.modules[name] = module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        out.append(sys.modules[name])
    return out


W, B, T = _modules()
MEASUREMENTS = ".shop/records/measurements/"
# a figure's noun -> the key of the measurement's figures that gives it
FIGURE = {"wall time": "wall_time", "session time": "session_time", "token": "tokens", "cost": "cost_by_role"}


def telemetry(step):
    node = step.request.node
    scenario = getattr(getattr(node, "obj", None), "__scenario__", None)
    return scenario is not None and Path(scenario.feature.filename).name == "telemetry.feature"


def ran(step):
    done = step.context["world"]
    assert done.code == 0, done.err
    return done


def kind_of(np):
    """The kind a noun phrase "the wall time w1" names."""
    return np.removeprefix("the ").rsplit(" ", 1)[0]


def grades(step):
    """{grade: the number of the scenario's review findings of it}."""
    found = {}
    for f in step.context.get("given", {}).get("review finding", {}).values():
        found[f.get("grade", "Important")] = found.get(f.get("grade", "Important"), 0) + 1
    return found


def written(step):
    done = ran(step)
    rel = done.out.strip().splitlines()[-1]
    if rel.startswith(MEASUREMENTS):
        assert done.record().is_file(), (step.text, done.out)
        return
    assert (done.repo / rel).is_file() and rel.startswith(".shop/batches/"), (step.text, rel)
    subject = T.git(step, "log", "-1", "--format=%s").strip()
    name = rel.rsplit("defect-", 1)[1].split(".")[0]
    assert subject.startswith("measure defect: ") and " d%s of " % name in subject, (step.text, subject)


def defect_field(step, key):
    done = ran(step)
    return W.field(done.repo / done.out.strip(), key)


def has(step):
    one, other = kind_of(step.subject), kind_of(step.nps[0])
    if (one, other) == ("item", "defect"):
        assert defect_field(step, "item") == B.ident(step.names[0]), step.text
    elif one == "batch" and other == "measurement":
        assert ran(step).figures()["batch"] == T.batch_name(step, step.names[0]), step.text
    elif other in FIGURE:
        assert ran(step).figures()[FIGURE[other]], step.text
    else:
        raise AssertionError("no reading of %r" % step.text)


def includes(step):
    figures, np = ran(step).figures(), step.nps[0]
    if np.startswith("the number of review findings"):
        grade = np.rsplit("`", 2)[1]
        assert figures["findings_by_grade"][grade] == grades(step).get(grade, 0), (step.text, figures["findings_by_grade"])
    else:
        assert figures[FIGURE[kind_of(np)]], step.text


@W.local("ThenDoes")
def then_does(step):
    if not telemetry(step) or step.term not in ("write", "has", "include", "for"):
        return False
    if step.term == "write":
        written(step)
    elif step.term == "has":
        has(step)
    elif step.term == "include":
        includes(step)
    else:
        assert defect_field(step, "batch") == T.batch_name(step, step.names[1]), step.text
    return None


@W.local("ThenPrints")
def prints(step):
    """`measure` prints the measurement m1 (the first batch compared), m2 (the second), and the ratio r1."""
    if not telemetry(step):
        return False
    out = ran(step).out
    for np in step.nps:
        if kind_of(np) == "measurement":
            rank = int(np.rsplit(" ", 1)[1].lstrip("m")) - 1
            assert step.context["compared"][rank] in out, (np, out)
        else:
            assert "ratio" in out, (np, out)
    return None
