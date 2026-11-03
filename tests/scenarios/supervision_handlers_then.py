"""Handlers of features/supervision.feature (design §14.3), the Thens on stages and what `work run` gave them, read
from the stand-in's record, log.jsonl, the stage directories, git and the run's output.

A scenario read off a trace (design-r2 §7.3) names a stage `work run` starts by its instance (`starts the stage s3`)
and gives its kind and node in the Thens after it (`the stage s3 is `plan``, `the stage s3 is for the work-item
w1`). Each such Then is a check kept for that instance and run again, narrower, as each later Then of the instance
adds its kind, node or branch; so every Then asserts what is known by then. A brief `work run` gave is kept by its
instance too, and a relation Then on the brief reads its text."""
import re
import sys

from vocab import handler

W, B, P = (sys.modules["shop_supervision_" + n] for n in ("world", "build", "plans"))
KIND = re.compile(r"`(%s)` stage" % "|".join(list(P.AGENTS) + list(P.ROUNDS)))
BRIEF = {"worker brief": ("Work-item: ", "PARTIAL", "never", "Result file:"), "review brief": ("tools size", "bindings"),
         "round brief": None}
WITH = {"work-item branch": "Work-item branch: work/", "commit": None, "request": "request"}


def bare(word):
    return word.strip("`")


def where(step):
    done = step.context.get("result")
    return (done.returncode, done.stdout[-3000:], done.stderr[-3000:]) if done else "no run"


def node_in(np):
    found = re.search(r"\b([a-z][a-z-]*\d+)$", np)
    return found.group(1) if found else None


def item(step):
    """The scenario's work-item: the first one its Givens wrote, else w1."""
    return next(iter(W.nodes(step.context, "work-item")), "w1")


def started(step, np):
    """The starts the stand-in recorded (or, for a `formulate` round, the stage directories) that `np` names."""
    repo, kind = step.repo, KIND.search(np)
    kind, node = (kind.group(1) if kind else None), node_in(np)
    if np.startswith(("an initiative", "the initiative")):
        return [p for p in (repo / W.WORK).glob("i*/initiative.md")
                if p.parent.name not in W.nodes(step.context, "initiative") and re.search(r"(?m)^fulfils: ", p.read_text())]
    if kind == "formulate":
        return list((repo / W.WORK).glob("*/runs/%s/*-formulate/result.json" % (node or "*")))
    found = W.starts(repo)
    if kind in P.ROUNDS:
        return [c for c in found if c["agent"].endswith("initiative-round") and "# %s of %s" % (kind, node or "") in c["brief"]]
    if kind:
        found = [c for c in found if c["agent"].endswith(P.AGENTS[kind])]
        node = None if kind in ("branch review", "analysis", "answer") else node
    if " on the work-item branch" in np:
        name = item(step)
        return [c for c in found if c["agent"].endswith("bdd-implementer")] if "kept work on %s" % name in W.git(
            repo, "log", "--all", "--format=%s") and W.git(repo, "branch", "--list", "work/" + name, check=False) == "" else []
    if node:
        found = [c for c in found if re.search(r"/%s\.md\b" % node, c["brief"])]
    return found


def instances(step):
    return W.sv(step.context).setdefault("new", {})


def stage_np(step, name):
    """The noun phrase a stage instance stands for, by what the Givens or the Thens so far say of it."""
    sv = W.sv(step.context)
    known = instances(step).get(name, {})
    kind = sv["stages"].get(name) or known.get("kind")
    node = sv["for"].get(name) or known.get("node")
    np = ("a `%s` stage" % kind if kind else "a stage") + (" for the node %s" % node if node else "")
    return np + (" on the work-item branch" if known.get("on") else "")


def defer(step, np, check):
    """Run `check` on the stage `np` names; for a stage instance, keep it to run again as later Thens narrow it."""
    found = re.fullmatch(r"the stage (s\d+)", np)
    if not found:
        return check(np)
    name = found.group(1)
    entry = instances(step).setdefault(name, {"checks": []})
    entry["checks"].append(check)
    return check(stage_np(step, name))


def narrow(step, name, **known):
    entry = instances(step).setdefault(name, {"checks": []})
    entry.update(known)
    for check in entry["checks"]:
        check(stage_np(step, name))


@handler("ThenDoes", "start")
def then_starts(step):
    def check(np):
        if KIND.search(np) and KIND.search(np).group(1) in P.ROUNDS and not node_in(np):
            return
        assert started(step, np), (step.text, np, W.starts(step.repo), where(step))
    defer(step, step.nps[-1], check)


@handler("ThenDoesNot", "start")
def then_starts_not(step):
    np = step.nps[-1]
    assert not started(step, np), (step.text, where(step))


@handler("ThenK_A", "stage")
def stage_is(step):
    narrow(step, step.names[0], kind=bare(step.values[0]))


def brief_of(step, np):
    found = started(step, np)
    assert found, (step.text, np, where(step))
    return found[0]


def give(step, np, what):
    """The check that `work run` gave the stage `np` names `what`; a brief given is kept by its instance."""
    if what.startswith("the file set"):
        text = (step.repo / step.context["nodes"][node_in(np)][1]).read_text()
        assert W.field(text, "fileset"), text
        return
    if KIND.search(np) is None and not node_in(np):
        return
    call = brief_of(step, np)
    brief, argv = call["brief"], call["argv"]
    kind = next((k for k in BRIEF if what.startswith(("a " + k, "the " + k))), None)
    if kind:
        for word in BRIEF[kind] or (("Line 1 text.", "recommended", "Answer: ", "Drafts path", "Kind: "),):
            assert (word in brief) if BRIEF[kind] else any(w in brief for w in word), (word, brief)
        name = node_in(what)
        if name:
            W.sv(step.context).setdefault("briefs", {})[name] = brief
    elif what == "a tool list":
        tools = argv[argv.index("--allowedTools") + 1].split(",")
        assert "Write" not in tools and "Edit" not in tools and argv[argv.index("--plugin-dir") + 1] == str(W.ROOT), argv
    elif "question" in what:
        assert P.QUESTION in brief, brief
    else:
        raise AssertionError("no reading of %s" % what)


@handler("ThenDoesTo", "give")
def then_gives(step):
    target, what = step.nps[-2], step.nps[-1]
    if not target.startswith(("the stage", "a ", "an ", "the `")):
        return give(step, target, what)
    defer(step, target if target.startswith(("the stage", "a ", "an ")) else "a %s" % target.split("the ", 1)[1],
          lambda np: give(step, np, what))


def subject(step):
    return re.match(r"the ([a-z -]+?) [a-z]+\d+ is ", step.text).group(1)


def brief_holds(step, word):
    name = step.names[0]
    brief = W.sv(step.context).get("briefs", {}).get(name)
    assert brief is not None, (step.text, "no brief %s was given" % name)
    return brief


@handler("ThenR", "for")
def then_for(step):
    kind = subject(step)
    if kind == "stage":
        return narrow(step, step.names[0], node=step.names[1])
    brief = brief_holds(step, "for")
    assert re.search(r"/%s\.md\b" % item(step), brief), brief


@handler("ThenR", "with")
def then_with(step):
    brief = brief_holds(step, "with")
    other = next(k for k in WITH if (" the %s " % k) in step.text + " ")
    if other == "commit":
        assert re.search(r"\b[0-9a-f]{7,40}\b", brief), brief
    else:
        assert WITH[other] in brief, (other, brief)


@handler("ThenR", "on")
def then_on(step):
    if subject(step) == "stage":
        return narrow(step, step.names[0], on=step.names[1])
    node = step.names[1]
    text = (step.repo / step.context["nodes"][node][1]).read_text()
    asked = text.split("\n## Questions\n", 1)[1].split("\n## ", 1)[0] if "\n## Questions\n" in text else ""
    if node.startswith("q"):     # a request's questions are numbered by line
        asked = text.split("## Questions", 1)[-1]
    assert asked.strip(), (text, where(step))


@handler("ThenDoes", "ask")
def then_asks(step):
    node = node_in(step.nps[-1])
    if node in step.context.get("nodes", {}):
        return then_on_node(step, node)


def then_on_node(step, node):
    text = (step.repo / step.context["nodes"][node][1]).read_text()
    assert "## Questions" in text, (text, where(step))
