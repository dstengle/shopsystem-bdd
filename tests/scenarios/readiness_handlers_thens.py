"""The Thens of features/readiness.feature in grammar 4 (b240 phase 20), one `local` handler of `ThenDoes` that takes a
step of readiness's scenarios (`mine`) and returns False on any other: refuse (the run exited 1, not a usage error),
name (what the Givens and the When said each thing is named by, or the item's status, in what the run printed),
write and holds (the item file the run changed holds the piece, the line under a fresh id with the id it retires
under `retired:`, or the block of the capability it recodified), commit (the run committed the item's file) and set
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


def written(step):
    """`work` writes ..., the item i1 holds ...: the item file the run wrote holds it."""
    held, line = _requirements(step), step.context["line"]
    if "recodified" in line:
        _block(held, line["recodified"])
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


THENS = {"refuse": lambda step: _done(step, 1), "name": named, "write": written, "holds": written,
         "commit": committed, "set": sets}


@local("ThenDoes")
def then_does(step):
    if not R.mine(step) or step.term not in THENS:
        return False
    THENS[step.term](step)
