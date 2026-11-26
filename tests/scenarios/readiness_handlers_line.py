"""The When of features/readiness.feature's `work line` scenarios in grammar 4 (b240 phase 20): `work line` run on an
item of the codified spec readiness_world.py writes, with the options the step names (b43's `--relation`,
`--universal`, `--upstream` and `--given`; b128's `--retires`; I19's `--recodify`; b220's `--recodify universal` and
`--universal --retires`; b271's `--no-line --retires`, on an item holding the passing line; b317's `--capability`),
each given what readiness_world says of it: a piece that conforms to its form unless a
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


def _changed(step, item, line, options):
    """b14's `--reword` or `--remove` of the requirement id a Given gave a requirement: the item's own line (the
    world's `work-queue#r5` of the passing line), or a live requirement of the capability (`work-queue#r1`)."""
    flag = "--reword" if "--reword" in options else "--remove"
    name = _name(options[flag])
    requirement = step.context.get("id_of", {}).get(name, name)     # by its id, or itself (the reword)
    owner = step.context.get("owner", {}).get(requirement, ("capability", None))
    if owner[0] == "item" and flag == "--remove" and step.context.get("held_ids"):
        ident = _history(step, item, line, step.context["held_ids"])
    elif owner[0] == "item":
        R.give_lines(step, item, R.PASSING)
        _shaped(step, item)
        ident = "%s#r5" % R.CAPABILITY
    else:
        R.codify(step)
        _shaped(step, item)
        ident = R.LIVE
    step.context.setdefault("says", {})[name] = ident
    line.update(changed=flag, ident=ident, old=R.PASSING)
    if flag == "--reword":      # a capability's live requirement, refused (r15); an item's own is drafting's r106
        return ["--reword", ident, R.LINE]
    return ["--remove", ident]


def _work(step, item, *args):
    """`work line` run on the item before the When, its new line's `<cap>#r<n>`, or None."""
    done = B.run_work(step, "line", B.ident(item), *args, **R.NO_INPUT)
    assert done.returncode == 0, (args, done.stdout, done.stderr)
    found = re.search(r"\b(%s#r\d+)\b" % R.CAPABILITY, done.stdout.split(":", 1)[1])
    return found.group(1) if found else None


def _history(step, item, line, held):
    """b323: the item, holding the live id the Givens' requirement id names (`R.LIVE`'s) under `retired:`, and the
    line the Givens' requirement names, made with `work line`. A line that retires the id writes both with
    `--retires`; one that does not is the defect's history (b323's notes): a `--retires` line of the same id written
    and removed, the id retired with `--no-line`, then a plain line given the reused id."""
    R.codify(step)
    B.write_item(step, item, status="shaped")
    name = next(iter(held))
    line["kept"] = R.LIVE.split("#")[1]
    step.context.setdefault("says", {})[name] = R.LIVE
    if step.context.get("retires_id", {}).get(name):
        line["kept"] = None
        return _work(step, item, "--retires", R.LIVE, R.PASSING)
    _work(step, item, "--remove", _work(step, item, "--retires", R.LIVE, R.LINE))
    _work(step, item, "--no-line", "--retires", R.LIVE)
    return _work(step, item, "--into", R.CAPABILITY, "--group", "Plain", R.PASSING)


NEW = ("shelf", "a person shelving things", "Things kept on a shelf, each found by its name.")


def _capability(step, item, line, value):
    """b317's `--capability`: a capability new to the fixture's spec (`NEW`), or its `work-queue` when a Given said
    the capability exists; the block the item is to hold kept as the piece written."""
    R.codify(step)
    _shaped(step, item)
    name, narrator, purpose = NEW
    if _name(value) in step.context.get("exists", ()):
        name = R.CAPABILITY
    step.context.setdefault("says", {})[_name(value)] = name
    line["piece"] = ("capability", "### %s\n\nnarrator: %s\ngroup: service\npurpose: %s" % (name, narrator, purpose))
    return ["--capability", name, "--narrator", narrator, purpose]


ENTRY = "- **shelf** (noun) → object shelf. A board things are kept on, each found by its name."


def _term(step, item, line):
    """b354's `--term` into an item holding a capability new to the context (a Given said it does not exist): the
    fixture's spec given a domain model (`spec/model/`, as `migrate init` founds a context), the item given the new
    capability (`NEW`) by `work line --capability`, and the vocabulary entry `ENTRY` kept as the piece written."""
    R.codify(step)
    _shaped(step, item)
    (step.repo / "spec" / "model").mkdir(exist_ok=True)
    name, narrator, purpose = NEW
    assert step.context.get("new"), "no Given said the capability does not exist: %s" % step.text
    _work(step, item, "--capability", name, "--narrator", narrator, purpose)
    _work(step, item, "--into", name, "--model", "object shelf\n  attributes: name (text)")   # its element (b810)
    line["piece"] = ("term", ENTRY)
    return ["--into", name, "--term", ENTRY]


@handler("WhenRuns", "`work line`")
def work_line(step):
    options = {code.strip("`"): value for code, value in step.options}
    item = _item(step)
    line = step.context["line"] = {"item": item, "options": options}
    if "--recodify" in options:
        value = options["--recodify"]
        capability = "universal" if value == "`universal`" else R.CAPABILITY
        R.universal(step) if capability == "universal" else R.codify(step, old=True)
        (step.repo / "spec" / "capabilities" / ("%s.md" % _name(value))).unlink(missing_ok=True)   # GivenK's file
        _shaped(step, item)
        line["recodified"] = capability
        args = ["--recodify", capability]
    elif "--capability" in options:
        args = _capability(step, item, line, options["--capability"])
    elif "--term" in options:
        args = _term(step, item, line)
    elif "--reword" in options or "--remove" in options:
        args = _changed(step, item, line, options)
    elif "--retires" in options and ("--universal" in options or "universal condition id" in options["--retires"]):
        R.universal(step)
        _shaped(step, item)
        line["retiring"] = _retired(step, options["--retires"], R.LIVE_U)
        line["written"] = R.CONDITION
        args = ["--universal", R.CONDITION, "--retires", line["retiring"]]
    elif "--retires" in options and "--no-line" in options:
        R.give_lines(step, item, R.PASSING)
        _shaped(step, item)
        line["retiring"] = _retired(step, options["--retires"], R.LIVE)
        line["no_line"] = True
        args = ["--no-line", "--retires", line["retiring"]]
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
