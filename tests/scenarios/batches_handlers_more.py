"""More handlers of features/batches.feature (workflow simplification plan 4): `work batch resume` and a park (Task
4), over the world batches_handlers.py loads; see there."""
import sys

from vocab import handler

W, B, T = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world"))
local = W.local
QUESTION = "Which reading holds?"


@handler("WhenRuns", "`work batch resume`")
def batch_resume(step):
    T.prepare(step)
    T.ensure_batch(step, resume=True)
    step.context["pending"] = [t for t in step.context["given"]["task"] if T.task_row(step, t)[0] == "pending"]
    T.run_batch(step, "resume", T.batch_name(step, step.names[-1]))


@handler("ThenDoes", "use")
def uses_plan(step):
    """The run named the batch's plan and every task of it, and each task that was pending is running in its
    worktree."""
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    batch = next(iter(step.context["given"]["batch"]))
    assert T.plan_rel(step, batch) in done.stdout, (step.text, done.stdout)
    for name in step.context["given"]["task"]:
        assert "\n%s " % T.task_id(step, name) in "\n" + done.stdout, (step.text, name, done.stdout)
    assert step.context["pending"], "no task was pending"
    for name in step.context["pending"]:
        status, branch = T.task_row(step, name)
        tree = step.repo / ".shop" / "worktrees" / ("%s-%s" % (T.batch_name(step, batch), T.task_id(step, name)))
        assert status == "running" and tree.is_dir(), (step.text, name, status, tree)
        assert T.git(step, "symbolic-ref", "--short", "HEAD", cwd=tree).strip() == branch


@handler("WhenHappens", "park")
def batch_parks(step):
    batch, item = step.names
    T.prepare(step)
    T.ensure_batch(step)
    T.run_batch(step, "park", T.batch_name(step, batch), B.ident(item), "--question", QUESTION)


@local("ThenDoes", "question")
def writes_question(step):
    """The last run gave an item's file a `## Question`; the question is that item's."""
    if step.term != "write" or not step.context.get("given"):
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    hits = [B.name_of(step.context, rel) for rel in filter(B.is_item_file, B.changed(step))
            if "\n## Question\n\n%s\n" % QUESTION in (step.repo / rel).read_text()]
    assert hits, (step.text, B.changed(step))
    step.context.setdefault("questions_written", {})[step.names[0]] = hits[0]


@local("ThenR", "question")
def question_on_item(step):
    question, item = step.names
    if step.term != "on" or question not in step.context.get("questions_written", {}):
        return False
    assert step.context["questions_written"][question] == item, (step.text, step.context["questions_written"])
    assert W.field(B.item_file(step, item), "status") == "needs-input", step.text
