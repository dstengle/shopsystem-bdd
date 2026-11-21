"""Task branches that touch one file (b491, reviews r7, r8): "the kept change k1 touches the file f1", "the kept change
k1 conflicts with the kept change k2" and "no kept change conflicts with a kept change", the kept changes the commits
batches_world makes on their items' branches. The file is `src/shared.txt`, nine lines committed on main before the
batch forks; a kept change that touches it alone (r7) changes its own line, each item's another, so the branches merge
in task order; a kept change that conflicts with another changes the first line otherwise, and one the scenario has
cite no item it may cite (`does not cite the item i5`) is a commit on the first item's branch. The Thens: the pull
request holds the kept change (its commit is on the pushed branch with the file as it changed it), and the refusal
names the file by its path and each item by its label. Loaded before batches_handlers_chore, whose touch is a chore's."""
import re
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
PATH = "src/shared.txt"
LINES = 9


def _shared(step):
    return step.context.setdefault("shared", {"touch": {}, "conflicts": {}, "not_cited": {}})


@four("GivenDoes", "touch", *BOTH)
def touches(step):
    """The kept change touches the shared file: written on main now, committed when the world is prepared."""
    (k1, commit), (k2, file) = parts(step)
    if (k1, k2) != ("commit", "file") or file in step.context.get("says", {}):
        return False
    _shared(step)["touch"][commit] = file
    path = step.repo / PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join("line %d\n" % n for n in range(1, LINES + 1)))


@four("GivenDoes", "conflict", *BOTH)
def conflicts(step):
    (_, one), (_, other) = parts(step)
    _shared(step)["conflicts"][one] = other


@four("GivenDoesNot", "conflict", *BOTH)
def conflicts_none(step):
    """No kept change conflicts with a kept change: each touches a line of its own."""
    _shared(step)


@four("GivenDoesNot", "cite", *BOTH)
def cites_not(step):
    (k1, commit), (k2, item) = parts(step)
    if (k1, k2) != ("commit", "item"):
        return False
    _shared(step)["not_cited"][commit] = item


def _item_of(step, commit):
    """The item whose branch holds the kept change: the one it cites, else the first in the batch it may cite."""
    found = step.context["given"].get("commit", {}).get(commit, {})
    if found.get("item"):
        return found["item"]
    barred = _shared(step)["not_cited"].get(commit)
    return next(i for i in step.context["given"]["item"] if i != barred and T.status_of(step, i) == "in-batch")


def _change(tree, commit, line):
    path = tree / PATH
    lines = path.read_text().splitlines(keepends=True)
    lines[line - 1] = "line %d changed by %s\n" % (line, commit)
    path.write_text("".join(lines))


def make_changes(step, name):
    """Each kept change of the shared file a commit on its item's branch of the batch `name`, citing the item."""
    shared = step.context.get("shared")
    if not shared:
        return
    clashing = set(shared["conflicts"]) | set(shared["conflicts"].values())
    commits = list(dict.fromkeys(list(shared["touch"]) + sorted(clashing)))
    for k, commit in enumerate(commits):
        item = _item_of(step, commit)
        branch = "%s-%s" % (T.batch_name(step, name), B.ident(item))
        tree = T.outside(step) / ("tree-%s-%s" % (branch, commit))
        T.git(step, "worktree", "add", "-q", str(tree), branch)
        _change(tree, commit, 1 if commit in clashing else min(1 + 4 * k, LINES))
        T.git(step, "commit", "-q", "-am", "%s changes the shared file\n\nItem: %s" % (commit, B.ident(item)), cwd=tree)
        step.context.setdefault("commits", {})[commit] = T.git(step, "rev-parse", "HEAD", cwd=tree).strip()
        T.git(step, "worktree", "remove", "--force", str(tree))


T.AFTER_BATCH.append(make_changes)


@four("ThenDoes", "holds", *BOTH)
def holds_change(step):
    """The pull request holds the kept change: its commit is on the pushed batch branch, the file as it changed it."""
    (k1, _), (k2, commit) = parts(step)
    if (k1, k2) != ("pull request", "commit") or "shared" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    pushed = T.git(step, "ls-remote", "origin", "refs/heads/%s" % T.batch_name(step, "b1")).split()[0]
    assert step.context["commits"][commit] in T.git(step, "rev-list", pushed).split(), step.text
    assert "changed by %s\n" % commit in T.git(step, "show", "%s:%s" % (pushed, PATH)), step.text


def _refused(step):
    done = step.context["result"]
    assert done.returncode == 1, (step.text, done.returncode, done.stdout, done.stderr)
    return done.stderr


@four("ThenDoes", "name", *BOTH)
@four("ThenDoesNot", "name", *BOTH)
def names(step):
    """The refusal names the file by its path, an item by its label `b<j> "<title>"`."""
    k, name = parts(step)[1]
    if k not in ("file", "item") or "shared" not in step.context:
        return False
    said = PATH if k == "file" else '%s "%s"' % (B.ident(name), step.context["item_fields"][name]["title"])
    named = said in _refused(step) if k == "file" else bool(re.search(re.escape(said), _refused(step)))
    assert named == (step.template == "ThenDoes"), (step.text, said, step.context["result"].stderr)
