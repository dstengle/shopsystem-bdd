"""The corpus of an amended item in features/batches.feature (r200, b740, b874): the scenario repository given a
corpus (`grammar/corpus/spec/`, the one corpus file `work-queue.md`), which the amend's apply writes the item's block
into; the Thens read off the item's task branch, its workspace's, after `work batch amend`: the corpus ending its last
block with one newline, holding the amended line. What an apply prepares is applying's (applying_handlers_prepare)."""
import sys

import backlog_items
import backlog_lines

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
CORPUS = "grammar/corpus/spec/work-queue.md"


def corpus(step, blocks=""):
    """The repository's corpus: its README and work-queue's file, with `blocks`."""
    R = sys.modules["shop_readiness_world"]
    R.codify(step)
    where = step.repo / "grammar" / "corpus" / "spec"
    where.mkdir(parents=True, exist_ok=True)
    (where / "README.md").write_text("# The spec corpus\n")
    (where / "work-queue.md").write_text("# work-queue: every live line with its intended reading\n%s" % blocks)


@four("GivenK", "logical form", *BOTH)
@four("GivenK", "requirement id", *BOTH)
@four("GivenK", "rule", *BOTH)
@four("GivenK", "construct", *BOTH)
def given_named(step):
    """A thing a later Given says what it is."""


@four("GivenDoes", "holds", *BOTH)
def holds_given(step):
    """This corpus holds the requirement: the repository keeps a corpus, which the lay writes the requirement's block
    into as its last (r172)."""
    if step.subject != "this corpus":
        return False
    elif not (step.repo / CORPUS).is_file():
        corpus(step)


def _line(step, name):
    """(id, line) of the item's one line, as the item holds it after the pick renumbered it."""
    item = backlog_items.find(step.repo, B.ident(name))
    blocks = backlog_lines.read(item, item.name)
    return next((rid, text) for b in blocks for g in b.groups for rid, text in g.requirements)


def _amended_corpus(step):
    """The corpus on the amended item's task branch after `work batch amend` (r200, b740), or None under another
    command."""
    done = step.context.get("result")
    if done is None or "amend" not in done.args or not (step.repo / CORPUS).is_file():
        return None
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    batch = T.batch_name(step, next(iter(step.context["given"]["batch"])))
    item = B.ident(next(iter(step.context["proposed"].values())))
    return T.git(step, "show", "%s-%s:%s" % (batch, item, CORPUS))


@four("ThenDoes", "conform", *BOTH)
def corpus_conforms(step):
    """`the corpus c1 conforms to the corpus form`: the task branch's corpus ends its last block with no blank line
    after it, the file ending in one newline."""
    text = _amended_corpus(step) if (parts(step)[0][0], step.nps[0]) == ("corpus", "the corpus form") else None
    if text is None:
        return False
    assert text == text.rstrip("\n") + "\n", (step.text, text[-200:])


@four("ThenDoes", "holds", *BOTH)
def workspace_holds_corpus(step):
    """`the workspace w1 holds the corpus c1`: the task's branch holds the corpus, with the amended item's line."""
    (k1, _), (k2, _) = parts(step)
    text = _amended_corpus(step) if (k1, k2) == ("worktree", "corpus") else None
    if text is None:
        return False
    _, line = _line(step, next(iter(step.context["proposed"].values())))
    assert "\n%s\n" % line in text, (step.text, line, text)
