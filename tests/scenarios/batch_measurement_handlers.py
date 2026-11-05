"""batch-measurement's handlers (design §14.3), for the lines left after `measure initiative` was retired (plan 9):
a measurement's example rows written by a Given, every `measure ...` command of the generated feature run as
`measure`'s main in-process on the World's day (batch_measurement_world.py), and the Thens reading what it printed
and the measurement it wrote.

`include "x"` holds when x is in the measurement's text; `not include "x"` when x is in none of its entries (its
stages, work-items, sessions and request; its totals are left out, since they always name every figure). `include
"x" for the logged stage l1` holds when x is a figure of that stage's entry, `not include` when it is not."""
import pathlib
import re
import shlex
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

from vocab import handler

from scenarios import batch_measurement_world as bw

FEATURE = HERE.parents[1] / "features" / "batch-measurement.feature"

def bare(word):
    return word.strip("`")


def world(step):
    if "world" not in step.context:
        step.context["world"] = bw.World(step.repo)
    return step.context["world"]


# --- Givens ---


@handler("GivenCodeText", "measurement")
def given_measurement(step):
    path = step.repo / ("%s.md" % bare(step.names[0]))
    path.write_text("# Measurement\n\n```json\n%s\n```\n" % step.docstring)


# --- the world a When runs in ---



def runs_measure(step):
    w = world(step)
    argv = shlex.split(bare(step.command))[1:] + step.context.get("flags", [])
    w.run(step.fixtures("monkeypatch"), step.fixtures("capsys"), *argv)


for _command in sorted(set(re.findall(r"When the person runs (`measure[^`]*`)", FEATURE.read_text()))):
    handler("WhenRuns", _command)(runs_measure)


# --- Thens ---


@handler("ThenPrints", "`measure`")
def prints(step):
    w = world(step)
    assert w.code == 0, w.err
    for np in step.nps:
        assert bare(np.strip('"')) in w.out, (np, w.out)


@handler("ThenPrintsNot", "`measure`")
def prints_not(step):
    w = world(step)
    assert w.code == 0, w.err
    for np in step.nps:
        assert np.strip('"') not in w.out, (np, w.out)


def stage_figures(w, name):
    """The figures of the stage a scenario names (`l1`): the keys of its entry."""
    item = w.called.get(name, name)
    found = [s for s in w.figures()["stages"] if s["work-item"] == item]
    assert len(found) == 1, (name, w.figures()["stages"])
    return found[0]


@handler("ThenDoes", "include")
def includes(step):
    w = world(step)
    assert w.code == 0, w.err
    if step.names:
        for q in step.quoted:
            assert q.strip('"') in stage_figures(w, step.names[0]), (q, step.text)
        return
    for np in step.nps:
        assert np.strip('"') in w.record().read_text(), (np, w.record().read_text())
