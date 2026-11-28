"""Handlers of batches' scenarios of an item applied to its task's workspace at opening (r194-r197, r202, b874), each
taking only a step of a scenario of one of its groups (`mine`), first in its key's chain. No adapter seam stands in
for the specification service: the When runs `work batch start` on the world batches_world.py prepares, the item i1
`ready`. Its apply and validation complete on readiness_world's passing line; they fail on a line citing a rule code
the repository's rule catalogue has no entry of (batches_handlers_broken's world: the applied workspace violates
`v_c1`, which the readiness bar's copy of `spec/` cannot see), so a requirement the Givens say violates a rule is such a
line, each in a group of its own, and one that does not violate it `PASS`; every rule a violated one, as the world has only it, and
a rule violated by none a code `work batch start` prints nowhere. The item i2 an item i1 depends on is `ready` with
`DEPENDED`. g195's item, which no Given gives a line, is given a broken one. The workspace of the item's task is its worktree `batch-<n>-t<k>` on its branch, both read off the batch's plan;
the Thens read that worktree, the task's branch and what `work batch start` printed."""
import re
import sys
from pathlib import Path

import backlog_items
import backlog_lines
import batch_git

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
GROUPS = {"g194", "g195", "g196", "g197", "g202"}
BROKEN = {"v_zz": "When the person runs `work check`, `work` shall print `v_zz`.",     # batches_handlers_broken's
          "v_zy": "When the person runs `work abandon`, `work` shall print `v_zy`."}     # each a trigger of its own
CODES = tuple(BROKEN)               # rule codes the rule catalogue has no entry of
PASS = "When the person runs `work tidy`, `work` shall exit successfully."     # no other group's trigger
DEPENDED = "When the person runs `work check`, `work` shall exit successfully."    # batches_handlers_limit's OWN
VIOLATED, UNNAMED = "v_c1", "v_zx9"     # the rule the applied workspace violates; a code printed nowhere
CAP = "work-queue"


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "batches" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("applied", {"rules": {}, "lines": {}})


def first(template, term):
    """`four`, the handler put first in its key's chain."""
    def mark(fn):
        four(template, term, "batches")(fn)
        chain = F.CHAINS[(template, term)]
        chain.insert(0, chain.pop())
        return fn
    return mark


@first("GivenK", "specification")
@first("GivenK", "rule")
def given_instance(step):
    """A specification (the spec of the task's workspace), a rule."""
    if not mine(step):
        return False


@first("GivenDoes", "has")
def given_has(step):
    """`the workspace w1 has the specification s1`; `the item i1 has the requirement r3`: a line of the item the
    When writes; the rest to the batches' and the backlog's handlers."""
    if not mine(step):
        return False
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) == ("worktree", "specification"):
        return None
    if (k1, k2) == ("item", "requirement"):
        world(step)["lines"].setdefault(n2, [n1, None])
        return None
    return False


@first("GivenDoes", "apply")
@first("GivenDoes", "validate")
def given_request(step):
    """`the batches service applies the item i1 to (validates) the specification s1`: the request the When's reply
    is on."""
    if not mine(step):
        return False
    world(step)["request"] = step.term


@first("GivenDoes", "violate")
@first("GivenDoesNot", "violate")
def given_violates(step):
    """`the requirement r3 violates the rule r2`: the line cites a rule code the catalogue has none of, so the applied
    workspace violates `v_c1`; `does not violate`: readiness_world's LINE, and the rule one violated by none."""
    if not mine(step):
        return False
    (_, requirement), (_, rule) = parts(step)
    w = world(step)
    if step.template == "GivenDoes":
        cited = CODES[sum(1 for line in w["lines"].values() if line[1] is not None and line[1] != "pass")]
        w["lines"][requirement][1] = cited
        w["rules"].setdefault(rule, VIOLATED)
    else:
        w["lines"][requirement][1] = "pass"
        w["rules"].setdefault(rule, UNNAMED)


def _tags(step):
    return set(sys.modules["vocab"].vocab4.requested.scenario(step.request.node).tags)


def _lines(step):
    """The item i1's lines: each requirement a Given names, else readiness_world's PASSING line, with the repository's
    rule catalogue written when one cites a rule code."""
    R = sys.modules["shop_readiness_world"]
    lines = [line for _, line in world(step)["lines"].values() if line is not None]
    if not lines and "g195" in _tags(step):     # validated with a line its workspace finds broken
        lines = [CODES[0]]
    if not lines:
        return
    R.codify(step)
    if any(line != "pass" for line in lines):
        catalogue = step.repo / "grammar" / "rules.md"
        catalogue.parent.mkdir(parents=True, exist_ok=True)
        catalogue.write_text("# The rule catalogue\n")
    texts = [PASS if line == "pass" else BROKEN[line] for line in lines]
    body = "### %s\n\n%s" % (CAP, "\n\n".join("#### [g%d] Title of i1, part %d\n- [r%d] %s" % (
        4 + k, k + 1, 5 + k, text) for k, text in enumerate(texts)))
    B.write_item(step, "i1", sections={"Requirements": body})


@first("WhenRuns", "`work batch start`")
@first("WhenHappens", "complete")
@first("WhenHappens", "fail")
def opens(step):
    """`the person opens the batch b1`, `the specification service completes (fails) the request to apply the item
    i1 to (validate) the specification s1`: `work batch start` run, the item i1 `ready`, and the item i2 it depends
    on `ready` with readiness_world's LINE."""
    if not mine(step):
        return False
    R = sys.modules["shop_readiness_world"]
    B.write_item(step, "i1", status="ready")
    if "i2" in step.context.get("items", {}):     # three items picked: a review limit they keep within
        step.context["delivery"] = T.DELIVERY + "\n[review]\nsize = 5000\n"
        step.context["own_line"] = PASS     # the world's own item's line, sharing no trigger with i1's
        B.write_item(step, "i2", status="ready")
        R.give_lines(step, "i2", DEPENDED, capability=CAP)
    _lines(step)
    T.before_start(step)
    T.prepare(step)
    T.run_batch(step, "start")


def _row(step, name):
    """(the plan's task id, its branch) of the item `name`'s task in `batch-1`'s plan, or (None, None)."""
    plan = step.repo / ".shop" / "batches" / "1" / "plan.md"
    text = plan.read_text() if plan.is_file() else ""
    found = re.search(r"(?m)^\| (t\d+) \| %s \| \S+ \| (\S+) \|$" % B.ident(name), text)
    return found.groups() if found else (None, None)


def _tree(step, name):
    """The worktree of the item `name`'s task, `batch-1-t<k>`, on its branch; refused unless it is."""
    task, branch = _row(step, name)
    assert task is not None, (step.text, step.context["result"].stdout, step.context["result"].stderr)
    tree = batch_git.trees_dir(step.repo) / ("batch-1-%s" % task)
    assert batch_git.is_tree(tree, branch), (step.text, tree, branch)
    return tree


def _done(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    return done


@first("ThenDoes", "has")
def then_has(step):
    """`the item i1 has the task t1`: the plan's task of the item; `the task t1 has the workspace w1`: its worktree on
    its branch; `the workspace w1 has the specification s1`: the worktree's spec holds the item's line, unbuilt, and
    no line of another item of the batch, the item's capability's feature a scenario of it."""
    if not mine(step) or "result" not in step.context:
        return False
    (k1, _), (k2, _) = parts(step)
    _done(step)
    if (k1, k2) == ("item", "task"):
        assert _row(step, "i1")[0], (step.text, step.context["result"].stdout)
    elif (k1, k2) == ("task", "worktree"):
        _tree(step, "i1")
    elif (k1, k2) == ("worktree", "specification"):
        _holds_own(step, _tree(step, "i1"))
    else:
        return False


def _holds_own(step, tree):
    """The worktree's spec holds each line of the item i1 as the base now holds it, unbuilt, and its feature a scenario
    of each; no line of another item of the batch."""
    item = backlog_items.find(step.repo, B.ident("i1"))
    others = [backlog_items.find(step.repo, i.name) for i in backlog_items.items(step.repo)
              if i.name != item.name and i.status == "in-batch"]
    spec = (tree / "spec" / "capabilities" / ("%s.md" % CAP)).read_text()
    unbuilt = [i.strip() for i in re.search(r"(?m)^unbuilt: \[(.*)\]$", spec).group(1).split(",")]
    feature = (tree / "features" / ("%s.feature" % CAP)).read_text()
    for block in backlog_lines.read(item, item.name):
        for rid, text in [r for g in block.groups for r in g.requirements]:
            assert "[%s] %s" % (rid, text) in spec and rid in unbuilt, (step.text, rid, spec[-600:])
            assert "@%s" % rid in feature, (step.text, rid, feature[-600:])
    assert others, step.text
    for other in others:
        for block in backlog_lines.read(other, other.name):
            for _, text in [r for g in block.groups for r in g.requirements]:
                assert text not in spec, (step.text, "another item's line", text)


@first("ThenDoes", "apply")
def then_applies(step):
    """`the batches service applies the item i1 to the specification s1`: taken with the `has` Then after it."""
    if not mine(step) or "result" not in step.context:
        return False
    _done(step)


@first("ThenDoes", "validate")
def then_validates(step):
    """`the batches service validates the specification s1 with the item i1`: the item given back `shaped` naming the
    rule its applied workspace violates, which only a validation of that workspace finds."""
    if not mine(step) or "result" not in step.context:
        return False
    done = _done(step)
    assert VIOLATED in done.stdout and B.status_of(step, B.ident("i1")) == "shaped", (step.text, done.stdout)


@first("ThenDoes", "reopen")
def then_reopens(step):
    """`the batches service reopens the item i1`: given back `shaped`, no task of it in the batch's plan."""
    if not mine(step) or "result" not in step.context:
        return False
    done = _done(step)
    assert B.status_of(step, B.ident("i1")) == "shaped", (step.text, done.stdout, done.stderr)
    assert _row(step, "i1") == (None, None), step.text


@first("ThenDoes", "name")
@first("ThenDoesNot", "name")
def then_names(step):
    """`the batches service names the rule r2` (does not name `r6`): its code in what `work batch start` printed."""
    if not mine(step) or "result" not in step.context or parts(step)[-1][0] != "rule":
        return False
    code, out = world(step)["rules"][parts(step)[-1][1]], _done(step).stdout
    assert (code in out) != (step.template == "ThenDoesNot"), (step.text, code, out)


@first("ThenDoes", "write")
@first("ThenDoes", "keep")
@first("ThenDoes", "cite")
def then_kept(step):
    """`the batches service keeps the kept change k1` and `the kept change k1 cites the item i1`: the head of the item's
    task branch a commit citing it, made at opening; `keeps the workspace w1`: the task's worktree."""
    if not mine(step) or "result" not in step.context:
        return False
    kinds = {k for k, _ in parts(step)}
    if "worktree" in kinds:
        _tree(step, "i1")
        return None
    if not {"kept change", "commit"} & kinds:
        return False
    _done(step)
    branch = _row(step, "i1")[1]
    assert branch, (step.text, step.context["result"].stdout)
    body = T.git(step, "log", "-1", "--format=%B", branch)
    assert "Item: %s" % B.ident("i1") in body.splitlines(), (step.text, body)


@first("ThenDoes", "holds")
def then_holds(step):
    """`the workspace w1 holds the requirement r1`: the dependent item's task worktree holds the line of the item it
    depends on, readiness_world's LINE, beside its own."""
    if not mine(step) or "result" not in step.context:
        return False
    (k1, _), (k2, _) = parts(step)
    if (k1, k2) != ("worktree", "requirement"):
        return False
    _done(step)
    R = sys.modules["shop_readiness_world"]
    spec = (_tree(step, "i1") / "spec" / "capabilities" / ("%s.md" % CAP)).read_text()
    assert DEPENDED in spec and R.PASSING in spec, (step.text, spec[-800:])
