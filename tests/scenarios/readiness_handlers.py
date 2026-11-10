"""Handlers of features/readiness.feature (plan 3, Task 2): `work ready` run with no input on the items backlog_world.py
writes, over the codified spec readiness_world.py writes. The item steps whose key the backlog claims reach these
through work_queue_world's `local` table, so test_readiness.py binds with `bind_all`; each returns False for a step
that is not about readiness, which then goes on to the registry."""
import importlib.util
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
local = W.local


@handler("WhenRuns", "`work ready`")
def work_ready(step):
    B.run_work(step, "ready", B.ident(step.names[-1]), **R.NO_INPUT)


@local("GivenK_C", "item")
def given_passing(step):
    """passing: the item given a line that passes the bar; not passing: one that does not parse, whose refusal must
    name the line's id and the word that stopped it; unworded: one whose scenario holds a step no Steps fun words,
    which the refusal must name (b46); ill-termed: a passing line beside a term bullet that brings a lexicon problem,
whose term the refusal must name. Any other condition (blocked) goes on to the backlog's."""
    word = step.text.split(" is ", 1)[1]
    if word == "ill-termed":
        R.give_lines(step, step.names[0], R.PASSING, [R.ILL_TERMED])
        step.context["ill_term"] = R.ILL_TERM
        return None
    if word == "unworded":
        R.give_lines(step, step.names[0], R.UNWORDED)
        step.context["unworded"] = R.UNWORDED_STEP
        return None
    if word not in ("passing", "not passing"):
        return False
    R.give_lines(step, step.names[0], R.PASSING if word == "passing" else R.FAILING)
    if word == "not passing":
        step.context["reason"] = ["work-queue#r5", "frobnicate"]


@local("ThenExitsErr", "reason")
def refused_with_reason(step):
    """The run was refused (exit 1, not a usage error), naming the item and every word of the reason a Given kept; a
    reason no readiness Given kept is another capability's (supervision's `work run`)."""
    if "reason" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 1, (done.returncode, done.stdout, done.stderr)
    labels = [said for name, said in step.context.get("says", {}).items() if B.item_rel(step.context, name)]
    assert labels and all(label in done.stderr for label in labels), (labels, done.stderr)
    for word in step.context.get("reason", ()):
        assert word in done.stderr, (word, done.stderr)


def _before(step, rel):
    """The file's text at the commit the run started from, or "" when it was not there."""
    try:
        return W.git(step.repo, "show", "%s:%s" % (step.context["head"], rel))
    except Exception:  # noqa: BLE001  (a file the run made)
        return ""


def _asks(before, after):
    """Whether a file's change asks a question: a `## Question` gained, an entry under `## Questions` added, or a
    status moved to `needs-input` or `awaiting-asker`."""
    def entries(text):
        found = text.split("\n## Questions\n", 1)
        return [x for x in found[1].split("\n## ", 1)[0].splitlines() if x.strip()] if len(found) > 1 else []

    def status(text):
        found = [x for x in text.split("\n---", 1)[0].splitlines() if x.startswith("status:")]
        return found[0].split(":", 1)[1].strip() if found else None
    if "\n## Question\n" in after and "\n## Question\n" not in before:
        return True
    if len(entries(after)) > len(entries(before)):
        return True
    return status(after) != status(before) and status(after) in ("needs-input", "awaiting-asker")


@handler("ThenDoesNot", "ask")
def asks_nothing(step):
    """D16: the command is there (not argparse's exit 2), no file the run changed asks a question, and no line it
    printed ends with a question mark."""
    done = step.context["result"]
    assert done.returncode != 2, ("the command is not there", done.stderr)
    for rel in W.runs(step)[-1]["changed"]:
        path = step.repo / rel
        after = path.read_text() if path.is_file() else ""
        assert not _asks(_before(step, rel), after), (step.text, rel)
    for said in (done.stdout + done.stderr).splitlines():
        assert not said.rstrip().endswith("?"), (step.text, said)


@local("ThenExitsErr", "step")
def refused_naming_step(step):
    """The run was refused (exit 1), naming the unworded step a Given kept, whole (b46)."""
    if "unworded" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 1, (done.returncode, done.stdout, done.stderr)
    assert step.context["unworded"] in done.stderr, (step.context["unworded"], done.stderr)


@local("ThenExitsErr", "term")
def refused_naming_term(step):
    """The run was refused (exit 1), naming the term of the problem the item's term bullet brought."""
    if "ill_term" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 1, (done.returncode, done.stdout, done.stderr)
    assert step.context["ill_term"] in done.stderr, (step.context["ill_term"], done.stderr)
