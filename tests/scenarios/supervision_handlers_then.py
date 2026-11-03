"""Handlers of features/supervision.feature (design §14.3), the Thens: what `work run` started, gave, merged, kept,
committed and printed, read from the stand-in's record, log.jsonl, the stage directories, git and the run's output.
A Then names a stage by its kind (a `research` stage) and the node it is for; a node's status is world_nodes.py's."""
import re
import sys

from vocab import handler

W, B, P = (sys.modules["shop_supervision_" + n] for n in ("world", "build", "plans"))
KIND = re.compile(r"`(%s)` stage" % "|".join(list(P.AGENTS) + list(P.ROUNDS)))


def bare(word):
    return word.strip("`")


def where(step):
    done = step.context.get("result")
    return (done.returncode, done.stdout[-3000:], done.stderr[-3000:]) if done else "no run"


def node_in(np):
    found = re.search(r"\b([a-z][a-z-]*\d+)$", np)
    return found.group(1) if found else None


def started(step, np):
    """The starts the stand-in recorded (or, for a `formulate` round, the stage directories) that `np` names."""
    repo, kind = step.repo, KIND.search(np)
    kind, node = (kind.group(1) if kind else None), node_in(np)
    if np.startswith("an initiative that fulfils"):
        return [p for p in (repo / W.WORK).glob("i*/initiative.md")
                if p.parent.name not in step.context.get("nodes", {}) and re.search(r"(?m)^fulfils: \S*%s$" % node, p.read_text())]
    if kind == "formulate":
        return list((repo / W.WORK).glob("*/runs/%s/*-formulate/result.json" % node))
    found = W.starts(repo)
    if kind in P.ROUNDS:
        return [c for c in found if c["agent"].endswith("initiative-round") and "# %s of %s" % (kind, node or "") in c["brief"]]
    if kind:
        found = [c for c in found if c["agent"].endswith(P.AGENTS[kind])]
        node = None if kind in ("branch review", "analysis", "answer") else node
    if " on the work-item branch" in np:
        return [c for c in found if c["agent"].endswith("bdd-implementer")] if "kept work on w1" in W.git(
            repo, "log", "--all", "--format=%s") and W.git(repo, "branch", "--list", "work/w1", check=False) == "" else []
    if node:
        found = [c for c in found if re.search(r"/%s\.md\b" % node, c["brief"])]
    return found


@handler("ThenDoes", "start")
def then_starts(step):
    assert started(step, step.nps[-1]), (step.text, W.starts(step.repo), where(step))


@handler("ThenDoesNot", "start")
def then_starts_not(step):
    assert not started(step, step.nps[-1]), (step.text, where(step))


def brief_of(step, np):
    found = started(step, np)
    assert found, (step.text, where(step))
    return found[0]


@handler("ThenDoesTo", "give")
def then_gives(step):
    target, what = step.nps[-2], step.nps[-1]
    if what == "the file set":
        text = (step.repo / step.context["nodes"][node_in(target)][1]).read_text()
        assert W.field(text, "fileset"), text
        return
    call = brief_of(step, target if "stage for" in target else "a %s" % target.split("the ", 1)[1])
    brief, argv = call["brief"], call["argv"]
    if what == "a worker brief":
        for word in ("Work-item: ", "PARTIAL", "never", "Result file:"):
            assert word in brief, (word, brief)
    elif what == "a tool list":
        tools = argv[argv.index("--allowedTools") + 1].split(",")
        assert "Write" not in tools and "Edit" not in tools and argv[argv.index("--plugin-dir") + 1] == str(W.ROOT), argv
        assert all(t.startswith(("Bash(python3", "Bash(git", "Bash(%s" % W.SCRIPTS)) for t in tools if t.startswith("Bash(")), tools
    elif what == "a question":
        assert P.QUESTION in brief, brief
    elif what == "a round brief":
        assert any(w in brief for w in ("Line 1 text.", "recommended", "Answer: ", "Drafts path")), brief
    elif what == "a review brief":
        assert "tools size" in brief and "bindings" in brief, brief
    else:
        raise AssertionError("no reading of %s" % what)


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
    assert merged(step) and not W.git(step.repo, "branch", "--list", "work/w1").strip(), (W.git(step.repo, "branch"), where(step))


@handler("ThenDoes", "keep")
def then_keeps(step):
    np = step.nps[-1]
    if "report" in np:
        found = list((step.repo / W.WORK / "i1/runs/w1").glob("*-implement/report.md"))
        assert found and found[0].read_text() == "the implementer's report\n", (found, where(step))
    else:
        assert W.git(step.repo, "branch", "--list", "work/w1").strip(), (W.git(step.repo, "branch"), where(step))


@handler("ThenDoes", "rerun")
def then_reruns(step):
    runs = B.flaky_runs(step.repo)
    assert runs.count("alone") == 1 and "with" in runs, (runs, where(step))


@handler("ThenDoes", "restore")
def then_restores(step):
    text = (step.repo / W.WORK / "i1/initiative.md").read_text()
    assert "changed by a worker" not in text, text
    assert not W.git(step.repo, "status", "--porcelain", "--", W.WORK).strip(), where(step)


@handler("ThenDoes", "log")
def then_logs(step):
    sv, np = W.sv(step.context), step.nps[-1]
    stage = KIND.search(np).group(1) if KIND.search(np) else sv["stages"].get(node_in(np) or "", "research")
    lines = [l for l in W.log_lines(step.repo) if l.get("stage") == stage.replace(" ", "-")
             and l.get("event") in ("start", "end")]
    events = {l.get("event") for l in lines}
    assert {"start", "end"} <= events and all(l.get("session") and l.get("time") and l.get("agent") for l in lines), lines


@handler("ThenDoes", "name")
def then_names(step):
    np, repo = step.nps[-1], step.repo
    if "transcript" in np:
        found = list((repo / W.WORK / "i1/runs/w1").glob("*-research/session.json"))
        assert found and "transcript" in found[0].read_text(), (found, where(step))
    else:
        text = (repo / W.WORK / "i1/w1.md").read_text()
        assert B.DELEGATION in text.split("## Answers", 1)[-1], text


@handler("ThenDoes", "ask")
def then_asks(step):
    node = node_in(step.nps[-1])
    text = (step.repo / step.context["nodes"][node][1]).read_text()
    asked = text.split("\n## Questions\n", 1)[1].split("\n## ", 1)[0] if "\n## Questions\n" in text else ""
    assert asked.strip(), (text, where(step))


def took(step, name):
    return any(name in line.split() for line in step.context["result"].stdout.splitlines())


@handler("ThenDoes", "take")
def then_takes(step):
    assert took(step, node_in(step.nps[-1])), where(step)


@handler("ThenDoesNot", "take")
def then_takes_not(step):
    assert not took(step, node_in(step.nps[-1])), where(step)


@handler("ThenDoes", "push")
def then_pushes(step):
    log = W.git(W.remote_dir(step.repo), "log", "--format=%s", "main")
    assert "notes.txt" in log.splitlines(), (log, where(step))


def drafted(step, kind):
    given = {rel for _, rel in W.nodes(step.context).items()}
    return [p for p in (step.repo / W.WORK).glob("*/*.md") if p.name != "initiative.md" and
            str(p.relative_to(step.repo)) not in given and W.field(p.read_text(), "kind") == kind]


@handler("ThenDoes", "draft")
def then_drafts(step):
    assert drafted(step, step.nps[-1].split(" ", 1)[1]), (W.git(step.repo, "log", "--stat", "--format=%s"), where(step))


@handler("ThenDoesNot", "draft")
def then_drafts_not(step):
    found = drafted(step, step.nps[-1].split(" ", 1)[1])
    assert not found, (found, where(step))


@handler("ThenDoes", "raise")
def then_raises(step):
    assert list((step.repo.parent / "catalogue-ctx" / W.WORK / "requests").glob("q*.md")), where(step)


@handler("ThenDoes", "remove")
def then_removes(step):
    assert W.git(step.repo, "worktree", "list", "--porcelain").count("worktree ") == 1, W.git(step.repo, "worktree", "list")
