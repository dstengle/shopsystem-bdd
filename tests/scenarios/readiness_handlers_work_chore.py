"""readiness's chore steps (r51-r54, b316), `local` handlers loaded after readiness_handlers_thens.py so that each is
tried first and returns False on a step not its own: a chore a Given puts in an item (its `## Chore`, what `work`
names it by), `work chore` run on an item (with a requirement line in it when a Given said the item holds one) and
`work line` on an item holding a chore; the Thens that `work` wrote the chore in the item file it committed."""
import importlib.util
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

FILES = ("scripts/tidy.py", "docs/guide/")
CHECK = "python3 -c 'import sys; sys.exit(0)'"
SECTION = "Files:\n%s\n\nCheck: `%s`" % ("\n".join("- %s" % f for f in FILES), CHECK)


def _chore(step):
    return any(np.startswith("the chore ") for np in step.nps)


@local("GivenDoes")
def given_holds_chore(step):
    """the item i1 holds the chore c1: the item written shaped with its `## Chore`; the chore named by its check."""
    if not R.mine(step) or step.term not in ("hold", "holds") or not _chore(step):
        return False
    R.codify(step)
    B.write_item(step, step.names[0], sections={"Notes": B.NOTE, "Chore": SECTION})
    step.context.setdefault("says", {})[step.names[-1]] = CHECK
    step.context["chore"] = step.names[0]
    return None


@local("GivenDoesNot")
def given_holds_no_requirement(step):
    """the item i1 holds no requirement: the item is written with no `## Requirements`, as it is."""
    if not R.mine(step) or step.term not in ("hold", "holds") or step.nps != ["no requirement"]:
        return False
    return None


def _item(step):
    return step.names[-1] if step.names else "i1"


@local("WhenRuns")
def work_chore(step):
    """`work chore` on the item, with a requirement line in it when a Given said it holds one; `work line` on an item
    that holds a chore, given a line that passes the bar."""
    if not R.mine(step) or step.term not in ("`work chore`", "`work line`"):
        return False
    item = _item(step)
    if step.term == "`work line`":
        if step.context.get("chore") != item:
            return False
        B.run_work(step, "line", B.ident(item), "--into", R.CAPABILITY, R.PASSING, **R.NO_INPUT)
        return None
    owned = [req for req, (kind, owner) in step.context.get("owner", {}).items() if kind == "item" and owner == item]
    if owned:
        R.give_lines(step, item, R.PASSING)
        for req in owned:
            step.context.setdefault("says", {})[req] = "%s#r5" % R.CAPABILITY
    B.write_item(step, item, status="shaped")
    args = [a for f in FILES for a in ("--file", f)] + ["--check", CHECK]
    B.run_work(step, "chore", B.ident(item), *args, **R.NO_INPUT)
    step.context["line"] = {"item": item}
    return None


@local("ThenDoes")
def then_chore(step):
    """`work` writes the chore c1, the item i1 holds the chore c1: the item file the run wrote holds the chore's
    files and check under `## Chore`."""
    if not R.mine(step) or step.term not in ("write", "holds") or not _chore(step):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    rel = B.bind_written(step, step.context["line"]["item"])
    text = (step.repo / rel).read_text()
    assert "\n## Chore\n\n%s\n" % SECTION in text, (step.text, text)
    return None
