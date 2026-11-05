"""Handlers of features/supervision.feature (design §14.3), the Thens on what `work run` merged, kept, logged, named,
took, pushed, drafted, raised and removed, and the Givens of what a stage holds (its resources are `work run`'s own
to take, so a Given of one builds nothing). The scenario's work-item is the one its Givens wrote (supervision_
handlers_then.item), whatever its name."""
import re
import sys

from vocab import handler

W, B, P = (sys.modules["shop_supervision_" + n] for n in ("world", "build", "plans"))


def where(step):
    done = step.context.get("result")
    return (done.returncode, done.stdout[-3000:], done.stderr[-3000:]) if done else "no run"


def node_in(np):
    found = re.search(r"\b([a-z][a-z-]*\d+)$", np)
    return found.group(1) if found else None


def item(step):
    return next(iter(W.nodes(step.context, "work-item")), "w1")


@handler("GivenHolds", "stage")
def stage_holds(step):
    """A Given stage's resource: held by `work run` when it runs the stage."""


def merged(step):
    return W.git(step.repo, "cat-file", "-e", "main:feature.txt", check=False) == "" and \
        "feature.txt" in W.git(step.repo, "ls-tree", "--name-only", "main")


@handler("ThenDoes", "merge")
def then_merges(step):
    assert merged(step), (W.git(step.repo, "log", "--format=%s", "main"), where(step))


@handler("ThenDoesNot", "merge")
def then_merges_not(step):
    assert not merged(step), where(step)


@handler("ThenDoes", "delete")
def then_deletes(step):
    assert merged(step) and not W.git(step.repo, "branch", "--list", "work/" + item(step)).strip(), (
        W.git(step.repo, "branch"), where(step))


@handler("ThenDoes", "keep")
def then_keeps(step):
    np = step.nps[-1]
    if "report" in np:
        found = list((step.repo / W.WORK / "i1/runs" / item(step)).glob("*-implement/report.md"))
        assert found and found[0].read_text() == "the implementer's report\n", (found, where(step))
    else:
        assert W.git(step.repo, "branch", "--list", "work/" + item(step)).strip(), (W.git(step.repo, "branch"), where(step))


@handler("ThenDoes", "rerun")
def then_reruns(step):
    runs = B.flaky_runs(step.repo)
    assert runs.count("alone") == 1 and "with" in runs, (runs, where(step))


@handler("ThenDoes", "restore")
def then_restores(step):
    text = (step.repo / W.WORK / "i1/initiative.md").read_text()
    assert "changed by a worker" not in text, text
    assert not W.git(step.repo, "status", "--porcelain", "--", W.WORK).strip(), where(step)


KIND = re.compile(r"`(%s)` stage" % "|".join(list(P.AGENTS) + list(P.ROUNDS)))


def kind_of(step, np):
    sv = W.sv(step.context)
    if KIND.search(np):
        return KIND.search(np).group(1)
    name = node_in(np) or ""
    return sv["stages"].get(name) or sv.get("new", {}).get(name, {}).get("kind") or "research"


@handler("ThenDoes", "log")
def then_logs(step):
    stage = kind_of(step, step.nps[-1])
    lines = [l for l in W.log_lines(step.repo) if l.get("stage") == stage.replace(" ", "-")
             and l.get("event") in ("start", "end")]
    events = {l.get("event") for l in lines}
    assert {"start", "end"} <= events and all(l.get("session") and l.get("time") and l.get("agent") for l in lines), lines


@handler("ThenDoes", "name")
def then_names(step):
    np, repo = step.nps[-1], step.repo
    if "transcript" in np:
        found = list((repo / W.WORK / "i1/runs" / item(step)).glob("*-research/session.json"))
        assert found and "transcript" in found[0].read_text(), (found, where(step))
    else:
        text = (repo / W.WORK / "i1" / ("%s.md" % item(step))).read_text()
        assert B.DELEGATION in text.split("## Answers", 1)[-1], text


def took(step, name):
    return any(name in line.split() for line in step.context["result"].stdout.splitlines())


def status(step, name):
    return W.field((step.repo / step.context["nodes"][name][1]).read_text(), "status")


@handler("ThenDoes", "take")
def then_takes(step):
    name = node_in(step.nps[-1])
    kind = step.context.get("nodes", {}).get(name, (None,))[0]
    if kind == "work-item":
        assert status(step, name) == "green", (name, status(step, name), where(step))
    elif kind is not None:
        assert took(step, name), where(step)


@handler("ThenDoesNot", "take")
def then_takes_not(step):
    name = node_in(step.nps[-1])
    kind = step.context.get("nodes", {}).get(name, (None,))[0]
    if kind == "work-item":
        before = W.sv(step.context).setdefault("given_status", {}).get(name)
        assert before is None or status(step, name) == before, (name, status(step, name), where(step))
    elif kind is not None:
        assert not took(step, name), where(step)


@handler("ThenDoes", "push")
def then_pushes(step):
    np = step.nps[-1]
    if np.startswith("the initiative branch"):
        log = W.git(W.remote_dir(step.repo), "log", "--format=%s", "main")
        assert "notes.txt" in log.splitlines(), (log, where(step))
        return
    if "unpushable" in W.sv(step.context)["conds"].get("remote", set()):
        return
    remote = W.git(W.remote_dir(step.repo), "rev-parse", "main").strip()
    assert remote == W.git(step.repo, "rev-parse", "main").strip(), where(step)


def drafted(step, kind):
    given = {rel for _, rel in W.nodes(step.context).items()}
    return [p for p in (step.repo / W.WORK).glob("*/*.md") if p.name != "initiative.md" and
            str(p.relative_to(step.repo)) not in given and W.field(p.read_text(), "kind") == kind]


def drafted_kind(np):
    return re.sub(r"^(a|an|the) ", "", re.sub(r" [a-z]+\d+$", "", np))


@handler("ThenDoes", "draft")
def then_drafts(step):
    assert drafted(step, drafted_kind(step.nps[-1])), (W.git(step.repo, "log", "--stat", "--format=%s"), where(step))


@handler("ThenDoesNot", "draft")
def then_drafts_not(step):
    found = drafted(step, drafted_kind(step.nps[-1]))
    assert not found, (found, where(step))


@handler("ThenDoes", "raise")
def then_raises(step):
    assert list((step.repo.parent / "catalogue-ctx" / W.WORK / "requests").glob("q*.md")), where(step)


@handler("ThenDoes", "remove")
def then_removes(step):
    assert W.git(step.repo, "worktree", "list", "--porcelain").count("worktree ") == 1, W.git(step.repo, "worktree", "list")
