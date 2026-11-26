"""A stand-in adapter of the laying service (b611), which `$SHOPSYSTEM_LAYING` names in batches' scenarios of
g179-g184: each request recorded as one JSON line in the file `$STAND_IN_LAYING_CALLS` names (its operation, the item
and the workspace), then answered as `$STAND_IN_LAYING_REPLY` says: unset, as the in-process adapter answers, so the
command behaves as it does with that adapter wired in; `complete`, a lay or a lift made of the in-process adapter and
its completion recorded (`completed`, with the operation it completes) before the reply, a check completed without
checking anything, its completion recorded; `fail`, a check failed naming each rule code `$STAND_IN_LAYING_RULES`
lists (comma-separated), whatever the workspace holds. `$STAND_IN_LAYING_ON`, when set, names the one operation the
reply is on, every other answered as the in-process adapter does. Loaded by laying from its path."""
import json
import os

import laying
import laying_inprocess as INPROCESS


def _record(operation, item, workspace, **more):
    with open(os.environ["STAND_IN_LAYING_CALLS"], "a", encoding="utf-8") as out:
        out.write(json.dumps({"operation": operation, "item": item.name, "workspace": str(workspace), **more}) + "\n")


def _reply(operation):
    on = os.environ.get("STAND_IN_LAYING_ON", "")
    return os.environ.get("STAND_IN_LAYING_REPLY", "") if on in ("", operation) else ""


def lay(item, workspace, command):
    _record("lay", item, workspace)
    done = INPROCESS.lay(item, workspace, command)
    if _reply("lay") == "complete" and done.outcome == "done":
        _record("completed", item, workspace, of="lay")
    return done


def lift(item, workspace, command, base=None):
    _record("lift", item, workspace)
    done = INPROCESS.lift(item, workspace, command, base)
    if _reply("lift") == "complete" and done.outcome == "done":
        _record("completed", item, workspace, of="lift")
    return done


def check(item, workspace):
    _record("check", item, workspace)
    if _reply("check") == "complete":
        _record("completed", item, workspace, of="check")
        return laying.done([])
    if _reply("check") == "fail":
        rules = [r for r in os.environ.get("STAND_IN_LAYING_RULES", "").split(",") if r]
        return laying.failed(["%s: %s a rule the laying service found violated" % (item.name, r) for r in rules])
    return INPROCESS.check(item, workspace)
