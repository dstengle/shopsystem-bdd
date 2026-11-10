"""The When of features/readiness.feature's `work line` scenarios in grammar 4 (b240 phase 20): `work line` run on an
item of the codified spec readiness_world.py writes, with the options the step names (b43's `--relation`,
`--universal`, `--upstream` and `--given`; b128's `--retires`; I19's `--recodify`; b220's `--recodify universal` and
`--universal --retires`), each given what readiness_world says of it: a piece that conforms to its form unless a
Given said it does not, a live id unless a Given said no requirement has it. What it ran is kept under `line` for
readiness_handlers_thens.py."""
import importlib.util
import re
import sys
from pathlib import Path

from vocab import handler


def shared(name, file):
    """A world module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
R = shared("shop_readiness_world", "readiness_world.py")

ITEM = "i1"


def _name(text):
    """The instance a noun phrase names (`the relation row r1`: r1), or None."""
    found = re.search(r"\b([a-z]+\d+)$", text or "")
    return found.group(1) if found else None


def _item(step):
    found = re.search(r" on the item (i\d+)$", step.text)
    return found.group(1) if found else ITEM


def _conforms(step, name):
    """False when a Given said the thing `name` does not conform to its form."""
    return all(ok for (thing, _), ok in step.context.get("conforms", {}).items() if _name(thing) == name)


def _retired(step, value, live):
    name = _name(value)
    return step.context.get("retires", {}).get(name, live) if name else live


def _shaped(step, item):
    B.write_item(step, item, status="shaped")


@handler("WhenRuns", "`work line`")
def work_line(step):
    options = {code.strip("`"): value for code, value in step.options}
    item = _item(step)
    line = step.context["line"] = {"item": item, "options": options}
    if "--recodify" in options:
        value = options["--recodify"]
        capability = "universal" if value == "`universal`" else R.CAPABILITY
        R.universal(step) if capability == "universal" else R.codify(step)
        (step.repo / "spec" / "capabilities" / ("%s.md" % _name(value))).unlink(missing_ok=True)   # GivenK's file
        _shaped(step, item)
        line["recodified"] = capability
        args = ["--recodify", capability]
    elif "--retires" in options and "--universal" in options:
        R.universal(step)
        _shaped(step, item)
        line["retiring"] = _retired(step, options["--retires"], R.LIVE_U)
        line["written"] = R.CONDITION
        args = ["--universal", R.CONDITION, "--retires", line["retiring"]]
    elif "--retires" in options:
        R.codify(step)
        _shaped(step, item)
        line["retiring"] = _retired(step, options["--retires"], R.LIVE)
        line["written"] = R.LINE
        args = ["--retires", line["retiring"], R.LINE]
    else:
        (flag,) = [f for f in options if f in R.PIECES]
        kind, good, bad = R.PIECES[flag]
        name = _name(options[flag])
        R.give_lines(step, item, R.PASSING)
        text = good if _conforms(step, name) else bad
        if text is bad:
            step.context.setdefault("says", {})[name] = text.splitlines()[0]
        line["piece"] = (kind, text)
        args = R.INTO.get(flag, []) + ([] if flag == "--given" else [flag]) + [text]
    B.run_work(step, "line", B.ident(item), *args, **R.NO_INPUT)
