"""The laying service, a driven port of the batches service (b611, b758, laying r2-r21; batches r179-r189; decisions
0125, 0133): the one module execution reaches the specification a batch works on through. `lay(item, workspace)` has
the item's lines and the other pieces of its `## Requirements` taken into the specification the workspace holds;
`prepare(workspace, batch, items)` has the workspace made whole for the batch once its items are laid, once for all
of them (their scenarios generated, the corpus, the catalogues, the Composition, the annotation and the decisions a
retirement supersedes); `lift(item, workspace)` has what a lay of the item took in taken out again; `check(item,
workspace)` has the item's requirements laid there checked against the rules of severity error. Each request answers
with its reply, a domain_envelope Response, which the caller handles: a lay, a prepare or a lift done (`done`, the
paths it changed and, of a prepare, the bookkeeping it gives back), a check done or failed (`failed`, one error a
reason, each naming the rule `rule:<code>` and the requirement `requirement:<cap>#r<n>` it is about); a failure outside
the operations' outcomes (a feature generator that does not answer) is raised as shop_refused's Refused. The adapter wired
in is the in-process one (laying_inprocess; decision 0125); `$SHOPSYSTEM_LAYING` names the file of another adapter run
in its place, a stand-in the tests swap in (`adapter`). `command` is the command a refusal is said as and `base` the
commit the batch was laid on, which a lift puts the operation tables back as."""
import importlib.util
import os

from domain_envelope import Response, error

ADAPTER = "SHOPSYSTEM_LAYING"
COMMAND = "work batch start"


def adapter():
    """The adapter of the port: the module of the file `$SHOPSYSTEM_LAYING` names, else the in-process one."""
    path = os.environ.get(ADAPTER)
    if not path:
        import laying_inprocess
        return laying_inprocess
    spec = importlib.util.spec_from_file_location("laying_adapter", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def lay(item, workspace, command=COMMAND):
    """The laying service's reply to a lay of the item in the workspace: done, {"changed": paths}."""
    return adapter().lay(item, workspace, command)


def prepare(workspace, batch, items, command=COMMAND):
    """The laying service's reply to a prepare of the workspace for the batch (its name) once its `items` are laid
    there: done, {"changed": paths, "unwritten": the catalogue problems, "superseded": (item, path, old id) of each
    decision it superseded}."""
    return adapter().prepare(workspace, batch, items, command)


def lift(item, workspace, command=COMMAND, base=None):
    """The laying service's reply to a lift of the item from the workspace: done, {"changed": paths}."""
    return adapter().lift(item, workspace, command, base)


def check(item, workspace):
    """The laying service's reply to a check of the item laid in the workspace: done, or failed naming each rule."""
    return adapter().check(item, workspace)


def done(changed, **more):
    """The reply of a lay, a prepare or a lift completed: done, with the paths changed."""
    return Response("done", dict(changed=list(changed), **more))


def failed(reasons):
    """The reply of a check failed: one error a reason (`<what>: <rule code> <label>...`), naming its rule."""
    return Response("failed", errors=[error(r, ["rule:%s" % code for code in codes(r)]) for r in reasons])


def codes(reason):
    """The rule code a reason names: the first word after its `: ` that is a rule's code."""
    import re
    found = re.search(r": (v[a-z0-9_]*)\b", reason)
    return [found.group(1)] if found else []


def reasons(reply):
    """The reasons of a failed check, as `work batch start` reopens an item with them."""
    return [e["reason"] for e in reply.errors]


def changed(reply, command=COMMAND):
    """The paths a lay, a prepare or a lift done changed; any other reply refused, naming what it says."""
    if reply.outcome != "done":
        from shop_files import Refused
        raise Refused("%s: the laying service answered %s: %s" % (
            command, reply.outcome, "; ".join(e["reason"] for e in reply.errors)))
    return reply.content["changed"]
