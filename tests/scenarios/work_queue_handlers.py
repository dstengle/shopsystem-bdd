"""Handlers of features/work-queue.feature (design §14.3): the `work` commands run on the nodes world_nodes.py
writes, in a git repository, and what they wrote, committed and printed read back.

The Givens of a note, an answer and a question keep the instance in the scenario's context (`things`); the When of
`work note` and `work answer` reads them for the text and the flag it runs with, and for the stage whose question it
answers. `ThenDoes` with `write` or `commit` matches the noun phrase against the files the last run changed or the
last commit holds (work_queue_world.matches), for every subject that runs a command in the repository.

The scenarios are read off the solver's traces (design-r2 §7), so the world maps the trace's names onto files: a node
the scenario names that no Given wrote is written before the command runs (work_queue_world.ensure_named), and the
name of a thing a Given introduced that the command then writes anew (`work add` numbers its own work-item) is bound
to the file the command wrote, at the first Then that names it written."""
import importlib.util
import sys
from pathlib import Path

from vocab import handler


def shared():
    """work_queue_world, loaded once by path."""
    name = "shop_work_queue_world"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name("work_queue_world.py"))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared()
local = W.local
NODES = next(m for m in list(sys.modules.values()) if getattr(m, "__file__", "").endswith("world_nodes.py"))
ASKED_FROM = {"research": "drafted", "plan": "researched", "implement": "claimed", "review": "done"}


def run_work(step, *args):
    """Run `work` in the repository, committed first, with every node the scenario names written; keep the result
    and the commit it started from."""
    W.ensure_named(step, NODES.write_node)
    step.context["head"] = W.init(step.repo)
    step.context["result"] = step.run("work", *args)
    return step.context["result"]


def bare(word):
    return word.strip("`")


def things_of(step, kind):
    return [(n, attrs) for n, (k, attrs) in step.context.get("things", {}).items() if k == kind]


@handler("GivenK_A", "note")
@handler("GivenK_A", "answer")
@handler("GivenK_A", "question")
def given_thing(step):
    step.context.setdefault("things", {})[step.names[0]] = (step.kind, {step.attribute: bare(step.values[0])})


@handler("GivenR", "kept in")
def kept_in(step):
    item, initiative = step.names
    kind, rel = step.context["nodes"][item]
    text = (step.repo / rel).read_text()
    (step.repo / rel).unlink()
    new = "%s/%s/%s.md" % (W.WORK, initiative, item)
    path = step.repo / new
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("part_of: initiative/%s" % W.initiative_of(step.context, item),
                                 "part_of: initiative/%s" % initiative))
    step.context["nodes"][item] = (kind, new)


@handler("WhenRuns", "`work add`")
def work_add(step):
    initiative = step.names[0]
    run_work(step, "add", initiative, "a work-item", "--part-of", "initiative/%s" % initiative, "--under", "thing",
             "--accepts", "thing#r1")


@handler("WhenRuns", "`work start`")
def work_start(step):
    run_work(step, "start", step.names[0])


@handler("WhenRuns", "`work list`")
@handler("WhenRuns", "`work show`")
def work_query(step):
    run_work(step, bare(step.term).split()[1], *step.names, *step.context.get("flags", []))


@handler("WhenRuns", "`work withdraw`")
@handler("WhenRuns", "`work retry`")
def work_move(step):
    item = step.names[0]
    W.ensure_named(step, NODES.write_node)
    initiative = W.initiative_of(step.context, item)
    status = W.field(step.repo / W.node_rel(step.context, item), "status")
    if item in step.context.get("out_of_step", ()):
        W.log(step.repo, initiative, item, "planned", "claimed")
    elif status == "failed":
        W.log(step.repo, initiative, item, "ready", "claimed")
        W.log(step.repo, initiative, item, "claimed", "failed")
    run_work(step, bare(step.term).split()[1], item)


@handler("WhenRuns", "`work note`")
def work_note(step):
    multi = any(a.get("form") == "multi-line" for _, a in things_of(step, "note"))
    run_work(step, "note", step.names[0], W.LINE_BREAK if multi else "next: the second stage")


@handler("WhenRuns", "`work answer`")
def work_answer(step):
    name = step.names[0]
    answer = dict(a for _, attrs in things_of(step, "answer") for a in attrs.items())
    stage = next((a["asking stage"] for _, a in things_of(step, "question")), None)
    if stage:
        W.log(step.repo, W.initiative_of(step.context, name), name, ASKED_FROM[stage], "awaiting-answer")
    text = W.LINE_BREAK if answer.get("form") == "multi-line" else "the answer"
    flag = [answer["flag"]] if answer.get("flag", "unflagged") != "unflagged" else []
    run_work(step, "answer", name, text, *flag)


def matched(step, rels):
    np = step.nps[-1]
    return [rel for rel in rels if W.matches(step.repo, step.context, np, rel)]


@handler("ThenDoes", "write")
def then_writes(step):
    runs = W.runs(step)
    assert runs, "no command ran: %s" % step.text
    changed = runs[-1]["changed"]
    hits = matched(step, changed)
    instance = W.named(step.nps[-1])
    if instance and instance[0] in W.PATHS and (not hits or not W.node_rel(step.context, instance[1])):
        hits = [rel for rel in changed if W.matches(step.repo, {}, "a %s" % instance[0], rel)]
        if hits:      # the trace's name for what the command wrote anew
            step.context.setdefault("nodes", {})[instance[1]] = (instance[0], hits[0])
    assert hits, (step.text, changed)


@handler("ThenDoes", "commit")
def then_commits(step):
    assert W.head(step.repo) != step.context.get("head"), "no commit was made: %s" % step.text
    files = W.committed(step.repo)
    assert matched(step, files), (step.text, files)


def expected_words(step):
    """What an error or an output must name, for each noun phrase of the step: what a Given said an instance or a
    noun phrase is named by (`says`), else a node's status or the instance's name."""
    words, says = [], step.context.get("says", {})
    for np in step.nps:
        kind = np[4:].rsplit(" ", 1)[0] if np.startswith("the ") and len(np.split()) > 2 else None
        article = kind and ("an " if kind[0] in "aeiou" else "a ") + kind     # the trace's `the origin o1`
        if np in says or article in says:
            words.append(says.get(np, says.get(article)))
        for name in (w for w in np.split() if w in step.names):
            kind = W.thing(step, name)[0]
            if name in says:
                words.append(says[name])
            elif np.startswith("the status of") and W.node_rel(step.context, name):
                words.append(W.field(step.repo / W.node_rel(step.context, name), "status"))
            elif np.startswith("the flag of"):
                words += ["--change", "--accept"]
            elif kind in ("note", "answer"):
                words.append("one line")
            elif W.node_rel(step.context, name) or kind:
                words.append(name)
    return words


@handler("ThenExitsErr", "`work`")
def work_refused(step):
    done = step.context["result"]
    assert done.returncode != 0, done.stdout
    for word in expected_words(step):
        assert word in done.stdout + done.stderr, (word, done.stderr)


@handler("ThenPrints", "`work`")
def work_prints(step):
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    for word in expected_words(step):
        assert word in done.stdout, (word, done.stdout)


@local("GivenK_C", "initiative")
def initiative_condition(step):
    """complete: a `green` work-item kept in the initiative; not complete, not open: what the Givens of its status
    and its work-items already make it; any other condition goes on to the registry's handler (design-model-check's)."""
    word = step.text.split(" is ", 1)[1]
    if word not in ("complete", "not complete", "not open"):
        return False
    if word == "complete":
        NODES.write(step.repo, "%s/%s/w9.md" % (W.WORK, step.names[0]), NODES.node_text(
            "work-item", "w9", "green", step.names[0]))


@local("GivenK_A")
def given_not(step):
    """`the request q1 is not `accepted``: the node keeps its status where it is another, else takes another of the
    attribute's values; any other Given goes on to the registry's handler."""
    if " is not " not in step.text or step.kind not in NODES.NODE_KINDS:
        return False
    rel = W.node_rel(step.context, step.names[0])
    if rel and W.field(step.repo / rel, "status") != bare(step.values[0]):
        return None
    other = next(v for v in ("open", "drafted", "started", "proposed") if v != bare(step.values[0]))
    NODES.write_node(step, step.kind, step.names[0], other)


@handler("ThenR", "fulfils")
def then_fulfils(step):
    initiative, request = step.names
    assert W.field(step.repo / W.node_rel(step.context, initiative), "fulfils") == NODES.full("request", request)


@handler("ThenR", "of")
def then_ledger_of(step):
    ledger, initiative = step.names
    assert W.node_rel(step.context, ledger) == "%s/%s/ledger.md" % (W.WORK, initiative), step.text
