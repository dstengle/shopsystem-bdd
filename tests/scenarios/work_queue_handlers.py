"""Handlers of features/work-queue.feature (design §14.3): the `work` commands run on the nodes world_nodes.py
writes, in a git repository, and what they wrote, committed and printed read back.

The Givens of a note, an answer and a question keep the instance in the scenario's context (`things`); the When of
`work note` and `work answer` reads them for the text and the flag it runs with, and for the stage whose question it
answers. `ThenDoes` with `write` or `commit` matches the noun phrase against the files the last run changed or the
last commit holds (work_queue_world.matches), for every subject that runs a command in the repository."""
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
ASKED_FROM = {"research": "drafted", "plan": "researched", "implement": "claimed", "review": "done"}


def run_work(step, *args):
    """Run `work` in the repository, committed first; keep the result and the commit it started from."""
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


@handler("GivenK_C", "work-item")
def given_out_of_step(step):
    step.context.setdefault("out_of_step", set()).add(step.names[0])


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


@handler("WhenRuns", "`work withdraw`")
@handler("WhenRuns", "`work retry`")
def work_move(step):
    item = step.names[0]
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
    stage = next((a["stage"] for _, a in things_of(step, "question")), None)
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
    assert matched(step, changed), (step.text, changed)


@handler("ThenDoes", "commit")
def then_commits(step):
    assert W.head(step.repo) != step.context.get("head"), "no commit was made: %s" % step.text
    files = W.committed(step.repo)
    assert matched(step, files), (step.text, files)


def expected_words(step):
    """What an error or an output must name, for each noun phrase of the step."""
    words = []
    for np in step.nps:
        for name in (w for w in np.split() if w in step.names):
            kind, attrs = W.thing(step, name)
            if np.startswith("the status of") and W.node_rel(step.context, name):
                words.append(W.field(step.repo / W.node_rel(step.context, name), "status"))
            elif np.startswith("the flag of"):
                words += ["--change", "--accept"]
            elif kind in ("note", "answer"):
                words.append("one line")
            else:
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
