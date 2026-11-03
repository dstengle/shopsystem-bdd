"""Handlers of features/supervision.feature (design §14.3), the Givens and the Whens: a Given of a stage, a result, a
session, a branch, a remote, a file, a change list or a question records what it says under `context["sv"]` (the
nodes are written by world_nodes.py, a delegation and an answer recorded by requests' and work-queue's handlers); a
When builds the repository around them (supervision_build.py), tells the stand-in claude what each session does
(supervision_plans.py) and runs `work run` once (supervision_world.py)."""
import importlib.util
import sys
from pathlib import Path

from vocab import handler


def load(name):
    """A helper module of this directory, loaded once by path."""
    key = "shop_" + name
    if key not in sys.modules:
        spec = importlib.util.spec_from_file_location(key, Path(__file__).with_name(name + ".py"))
        sys.modules[key] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[key]


W = load("supervision_world")
B = load("supervision_build")
P = load("supervision_plans")
B.W = P.W = W
OWN = ("session", "result", "remote", "initiative branch", "work-item branch", "file", "change list", "question")


def bare(word):
    return word.strip("`")


@handler("GivenK_A", "stage")
def given_stage(step):
    W.sv(step.context)["stages"][step.names[0]] = bare(step.values[0])


@handler("GivenK_A", "result")
def given_result(step):
    W.sv(step.context)["results"][step.names[0]] = bare(step.values[0])


@handler("GivenK", "result")
def given_bare_result(step):
    W.sv(step.context)["results"].setdefault(step.names[0], None)


@handler("GivenK", "session")
def given_session(step):
    W.sv(step.context)["sessions"][step.names[0]] = True


@handler("GivenK", "question")
def given_question(step):
    W.sv(step.context)["questions"].setdefault(step.names[0], (None, False))


for _kind in ("remote", "initiative branch", "work-item branch", "file", "change list", "draft", "transition", "worker",
              "worktree"):
    @handler("GivenK", _kind)
    def given_thing(step):
        W.sv(step.context).setdefault("things", {})[step.names[0]] = step.kind


def condition(step):
    """The condition word of a `the K x is [not] c` step, with "not " before it when it is negated."""
    word = step.text.split(" is ", 1)[1]
    return word


for _kind in OWN:
    @handler("GivenK_C", _kind)
    def given_condition(step):
        sv, name, word = W.sv(step.context), step.names[0], condition(step)
        sv.setdefault("inst", {}).setdefault(name, set()).add(word)
        sv["conds"].setdefault(step.kind, set()).add(word)
        if step.kind == "file" and word == "dirty":
            sv.setdefault("dirty", []).append(bare(name))
        if step.kind == "question":
            on, _ = sv["questions"].get(name, (None, False))
            sv["questions"][name] = (on, word == "answered")


@handler("GivenR", "for")
def stage_for(step):
    W.sv(step.context)["for"][step.names[0]] = step.names[1]


@handler("GivenR", "with")
def stage_with(step):
    W.sv(step.context)["with"][step.names[0]] = step.names[1]


@handler("GivenR", "on")
def question_on(step):
    sv = W.sv(step.context)
    _, answered = sv["questions"].get(step.names[0], (None, False))
    sv["questions"][step.names[0]] = (step.names[1], answered)


@handler("GivenR", "blocked by")
def blocked_by(step):
    W.sv(step.context)["blocked"][step.names[0]] = step.names[1]


def deliver(step, args, stage=None):
    """Build the repository, tell the stand-in what to do, and run `work run <args>` once."""
    sv = W.sv(step.context)
    sv.setdefault("inst", {})
    B.build(step.repo, step.context)
    plan = P.plan_for(step.repo, step.context, stage)
    return W.run_work(step.repo, step.context, plan, args)


def initiative_args(step, node):
    """The arguments of `work run` for a stage of `node`: none for a request, else the node's initiative."""
    if (step.context.get("nodes", {}).get(node) or ("",))[0] == "request":
        return []
    return ["i1"]


@handler("WhenRuns", "`work run`")
def runs_work_run(step):
    if step.subject and step.subject.startswith("the worker"):
        step.context["env"] = W.BY_WORKER
        return deliver(step, ["i1"])
    return deliver(step, [n for n in step.names if n.startswith("i")])


@handler("WhenHappens")
def happens(step):
    sv = W.sv(step.context)
    stage = next((n for n in step.names if n in sv["stages"]), None)
    node = sv["for"].get(stage, "w1") if stage else "w1"
    if sv["questions"].get(node):
        node = sv["questions"][node][0] or "w1"
    return deliver(step, initiative_args(step, node), stage)
