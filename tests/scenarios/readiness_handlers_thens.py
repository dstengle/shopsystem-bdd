"""The Thens of features/readiness.feature in grammar 4 (b240 phase 20), one `local` handler of `ThenDoes` that takes a
step of readiness's scenarios (`mine`) and returns False on any other: refuse (the run exited 1, not a usage error),
name (what the Givens and the When said each thing is named by, or the item's status, in what the run printed),
write and holds (the item file the run changed holds the piece, the line under a fresh id with the id it retires
under `retired:` (with `--no-line`, no line added), or the block of the capability it recodified), commit (the run committed the item's file) and set
(the item's status, or the language of the capability's block in the item, the capability's own file untouched)."""
import importlib.util
import re
import sys
from pathlib import Path


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
local = W.local


def _done(step, code=0):
    done = step.context["result"]
    assert done.returncode == code, (step.text, done.returncode, done.stdout, done.stderr)
    return done


def _requirements(step):
    """The `## Requirements` of the item file the run wrote."""
    _done(step)
    rel = B.bind_written(step, step.context["line"]["item"])
    return (step.repo / rel).read_text().split("\n## Requirements\n", 1)[1]


def _block(held, capability):
    assert "\n### %s\n" % capability in "\n" + held, (capability, held)
    return held.split("### %s\n" % capability, 1)[1].split("\n### ", 1)[0]


def _retiring(step, held):
    """The new line under a fresh id of its block, the id it retires under the block's `retired:`, the new id
    printed."""
    line = step.context["line"]
    capability, old = line["retiring"].split("#")
    block = _block(held, capability)
    assert re.search(r"(?m)^retired: \[%s\]$" % old, block), block
    found = re.search(r"(?m)^- \[([rU][1-9]\d*)\] %s$" % re.escape(line["written"]), block)
    assert found and found.group(1) != old, block
    assert "%s#%s" % (capability, found.group(1)) in step.context["result"].stdout, step.context["result"].stdout


def _bare(step, held):
    """`--no-line --retires` (b271): the id it retires under the block's `retired:`, printed."""
    capability, old = step.context["line"]["retiring"].split("#")
    assert re.search(r"(?m)^retired: \[%s\]$" % old, _block(held, capability)), held
    assert step.context["line"]["retiring"] in step.context["result"].stdout, step.context["result"].stdout


def _unwritten(step):
    """`work` does not write the requirement r2 (b271): the item's lines are the one it held, no line added."""
    held = _requirements(step)
    assert re.findall(r"(?m)^- \[r[1-9]\d*\] (.*)$", held) == [R.PASSING], held


def written(step):
    """`work` writes ..., the item i1 holds ...: the item file the run wrote holds it."""
    held, line = _requirements(step), step.context["line"]
    if "recodified" in line:
        _block(held, line["recodified"])
    elif line.get("no_line"):
        _bare(step, held)
    elif "retiring" in line:
        _retiring(step, held)
    else:
        kind, text = line["piece"]
        if kind == "universal condition":
            assert re.search(r"(?m)^- \[U[1-9]\d*\] %s$" % re.escape(text), held), held
        elif kind == "upstream entry":
            assert re.search(r"(?m)^- %s$" % re.escape(text), held), held
        else:
            assert all(re.search(r"(?m)^%s$" % re.escape(x), held) for x in text.splitlines()), (text, held)


def named(step):
    """What the run printed names each thing the step names: by what a Given or the When said it is named by, or,
    of the status of an item, by the status the item file has."""
    done = step.context["result"]
    said = done.stdout + done.stderr
    for np in step.nps:
        name = np.rsplit(" ", 1)[-1]
        if np.startswith("the status of the item "):
            word = B.fields_of(step, name)["status"]
        else:
            word = step.context.get("says", {}).get(name)
        assert word and word in said, (step.text, word, said)


def committed(step):
    rel = B.bind_written(step, step.context.get("line", {}).get("item", step.names[0]))
    files = W.git(step.repo, "diff", "--name-only", step.context["head"], "HEAD").split()
    assert rel in files, (step.text, files)


def sets(step):
    """sets the status of the item i1 to `ready`; sets the language of the capability c1 (or of `universal`) to
    `codified-2` in the item's block for it, and its own file still `codified-1`."""
    value = step.values[0].strip("`")
    if step.nps[0].startswith("the status of the item "):
        _done(step)
        assert B.fields_of(step, step.names[0])["status"] == value, step.text
        return
    capability = step.context["line"]["recodified"]
    assert re.match(r"\nlanguage: %s$" % value, _block(_requirements(step), capability), re.MULTILINE), step.text
    own = "spec/universal.md" if capability == "universal" else "spec/capabilities/%s.md" % capability
    assert "language: codified-1" in (step.repo / own).read_text(), own


def removed(step):
    """`work` removes the requirement r1: the item file the run wrote no longer holds its line; with `--remove`, nor
    the requirement's id, nor its group, whose last line it was."""
    held, line = _requirements(step), step.context["line"]
    assert line["old"] not in held, held
    if line["changed"] == "--remove":
        rid = line["ident"].split("#")[1]
        assert "[%s]" % rid not in held and "[g4]" not in held, held
    if line.get("kept", ()) is None:       # b323: the id the line retired, out of `retired:` with it
        assert "retired:" not in held, held


def kept(step):
    """b323's `work` does not remove the requirement id r3: the id stays under the item's block's `retired:`."""
    held = _requirements(step)
    assert re.search(r"(?m)^retired: \[%s\]$" % step.context["line"]["kept"], held), (step.text, held)


def keeps(step):
    """b281's `work` keeps the item i1 of `work ready` on a ready item: the run made no commit of its file, which
    still holds the status the Givens wrote."""
    _done(step)
    name = step.names[0]
    rel = B.item_rel(step.context, name)
    head = step.context.get("head")
    assert rel and head and rel not in W.git(step.repo, "diff", "--name-only", head, "HEAD").split(), (step.text, rel)
    assert W.field(step.repo / rel, "status") == step.context["item_fields"][name]["status"], step.text


THENS = {"refuse": lambda step: _done(step, 1), "name": named, "write": written, "holds": written,
         "commit": committed, "set": sets, "remove": removed, "keep": keeps}


@local("ThenDoesNot")
def then_does_not(step):
    """`work` does not name the bar check b3 (a counter-example, b273): what it is named by is not in the output;
    does not write the requirement r2 (b271): no line added to the item; does not remove the requirement id r3
    (b323): the id kept under `retired:`."""
    if not R.mine(step) or step.term not in ("name", "write", "remove"):
        return False
    if step.term == "remove":
        return kept(step)
    if step.term == "write":
        return _unwritten(step)
    done = step.context["result"]
    for np in step.nps:
        word = step.context.get("says", {}).get(np.rsplit(" ", 1)[-1])
        assert word and word not in done.stdout + done.stderr, (step.text, word)
    return None


@local("ThenDoes")
def then_does(step):
    if not R.mine(step) or step.term not in THENS:
        return False
    THENS[step.term](step)
