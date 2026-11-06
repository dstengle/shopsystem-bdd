"""The scenario repository of features/batches.feature (not a handler module, so the glob does not load it): the
codified spec readiness_world.py writes, the items backlog_world.py writes, a bare repository beside it as `origin`,
the stand-in gh (tests/scripts/stub_gh.py), and the batches, tasks, commits and pull requests a scenario names, built
before its command runs (workflow simplification plan 4, D21, D22). batches_handlers.py loads it by path as
`shop_batches_world`.

A scenario's batch `b1` is `batch-1`, its task `t1` the plan's `t1`, its commit `c1` a commit on its item's branch.
Under `work batch start` the world adds its own ready, passing item `i92` (D21). Under any other command it builds
what the scenario names: a task with no status Given is `done`, but `pending` under `work batch resume` (D22); a batch
whose items the scenario does not make `in-batch` gets the world's own `i93`, with a cited commit and a task of its
own; a pull request makes its batch `in-review`."""
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

import backlog_items
import backlog_lines
import batch_start
import spec_unbuilt

STUB = Path(__file__).resolve().parents[1] / "scripts" / "stub_gh.py"
DELIVERY = '[batch]\ntests = "python3 -c pass"\n'
SECOND = "When the person runs `work abandon` on an initiative that is `started`, `work` shall exit successfully."
OWN_START, OWN_IN = "i92", "i93"
URL = "https://github.com/ex/ctx/pull/%d"
CAP = "spec/capabilities/work-queue.md"


def W():
    return sys.modules["shop_work_queue_world"]


def B():
    return sys.modules["shop_backlog_world"]


def R():
    return sys.modules["shop_readiness_world"]


def outside(step):
    """A directory beside the repository: the bare remote and the stand-in gh's files."""
    if "outside" not in step.context:
        step.context["outside"] = step.request.getfixturevalue("tmp_path_factory").mktemp("outside")
    return step.context["outside"]


def env(step):
    where = outside(step)
    return dict(os.environ, SHOPSYSTEM_WORK_GH="%s %s" % (shlex.quote(sys.executable), shlex.quote(str(STUB))),
                STUB_GH_CALLS=str(where / "gh-calls.jsonl"), STUB_GH_STATE=str(where / "gh-state.json"),
                GH_TOKEN="", GIT_TERMINAL_PROMPT="0")


def gh_calls(step):
    path = outside(step) / "gh-calls.jsonl"
    return [json.loads(line)["argv"] for line in path.read_text().splitlines()] if path.is_file() else []


def git(step, *args, cwd=None):
    return W().git(cwd or step.repo, *args)


def prepare(step):
    """Once: the codified spec, `.shop/delivery.toml`, every item the scenario names, all committed, and `origin` a
    bare repository with `main` pushed."""
    if step.context.get("prepared"):
        return
    R().codify(step)
    (step.repo / ".shop").mkdir(exist_ok=True)
    (step.repo / ".shop" / "delivery.toml").write_text(step.context.get("delivery", DELIVERY))
    B().index(step)
    B().ensure_items(step)
    W().init(step.repo)
    bare = outside(step) / "origin.git"
    W().git(outside(step), "init", "-q", "--bare", str(bare))
    git(step, "remote", "add", "origin", str(bare))
    git(step, "push", "-q", "origin", "main")
    step.context["prepared"] = True


def given(step, kind, name):
    """What the Givens said of the scenario's batch, task, commit or pull request `name`."""
    return step.context.setdefault("given", {}).setdefault(kind, {}).setdefault(name, {})


def status_of(step, name):
    return (step.context.get("item_fields", {}).get(name) or {}).get("status")


def has_lines(step, name):
    return "Requirements" in (step.context.get("item_fields", {}).get(name) or {}).get("sections", {})


def before_start(step):
    """Under `work batch start`: the world's own ready, passing item (D21), and every ready item the scenario names
    with no lines given a passing line."""
    for name in list(step.context.get("items", {})):
        if status_of(step, name) == "ready" and not has_lines(step, name):
            R().give_lines(step, name, R().PASSING)
    B().write_item(step, OWN_START, title="an item the world readies", status="ready")
    R().give_lines(step, OWN_START, SECOND)


def batch_name(step, name):
    return step.context.setdefault("batches", {}).setdefault(name, "batch-%s" % re.sub(r"^\D+", "", name))


def named(step, kind):
    return list(dict.fromkeys(re.findall(r"\bthe %s ([a-z]+\d+)\b" % kind, " ".join(W().scenario_texts(step)))))


def ensure_batch(step, resume=False):
    """Before a When that is not `start`: every batch, task, commit and pull request the scenario names is built."""
    batches = [n for n in named(step, "batch") if n not in step.context.get("plans", ())]
    for name in batches or ["b1"]:
        given(step, "batch", name)
    tasks = step.context["given"].setdefault("task", {})
    for name in named(step, "task"):
        tasks.setdefault(name, {})
    first = next(iter(step.context["given"]["batch"]))
    for name, found in step.context["given"].setdefault("item", {}).items():
        found.setdefault("batch", first)
    in_batch = [n for n in step.context["given"]["item"] if status_of(step, n) == "in-batch"]
    for name in [n for n in step.context.get("items", {}) if status_of(step, n) == "in-batch"]:
        if name not in step.context["given"]["item"]:
            step.context["given"]["item"][name] = {"batch": first}
            in_batch.append(name)
    if not in_batch:
        B().write_item(step, OWN_IN, title="an item the world builds", status="in-batch")
        step.context["given"]["item"][OWN_IN] = {"batch": first}
    for name, found in tasks.items():
        found.setdefault("batch", first)
        found.setdefault("item", OWN_IN if OWN_IN in step.context["given"]["item"] else next(
            (n for n, f in step.context["given"]["item"].items() if f["batch"] == found["batch"]), OWN_IN))
        found.setdefault("status", "pending" if resume else "done")
    for name, found in step.context["given"]["item"].items():
        if not any(t["item"] == name for t in tasks.values()):
            tasks["_%s" % name] = {"batch": found["batch"], "item": name, "status": "pending" if resume else "done"}
    for name in step.context["given"]["batch"]:
        make_batch(step, name)


def give_batch_lines(step, items):
    """Each item of a batch that has no lines given one, in work-queue, with a group and an id of its own."""
    for item in items:
        if has_lines(step, item):
            continue
        k = step.context["laid_count"] = step.context.get("laid_count", 0) + 1
        fields = step.context["item_fields"][item]
        lines = "### work-queue\n\n#### [g%d] %s\n- [r%d] %s" % (3 + k, fields["title"], 4 + k, (R().PASSING, SECOND)[k % 2])
        B().write_item(step, item, sections=dict(fields.get("sections", {}), Requirements=lines))


def lay(step, tree, items):
    """The lines commit of a batch, as `work batch start` makes it: every item's lines laid, their ids unbuilt, the
    features written again, citing each item (plan 4 review, B1)."""
    found = [backlog_items.find(step.repo, B().ident(i)) for i in items]
    changed = batch_start.lay_lines(tree, found)
    git(step, "add", "--", *changed, cwd=tree)
    git(step, "commit", "-q", "-m", "%s: the requirement lines\n%s" % (tree.name, batch_start.cites(found)), cwd=tree)
    step.context.setdefault("laid", {}).update(
        {i: [g.id for b in backlog_lines.read(f, i) for g in b.groups] for i, f in zip(items, found)})


def built(tree, item):
    """The item's ids taken out of `unbuilt:` in the worktree, as its task's commits would."""
    path = tree / CAP
    ids = [r.split("#")[1] for r in backlog_lines.ids(backlog_lines.read(item, item.name))]
    path.write_text(spec_unbuilt.without_unbuilt(path.read_text(), ids))


def make_batch(step, name):
    """The batch `name` written by hand: `batch-<n>` made from main with the lines commit of its items (`lay`), one
    branch for each item with one commit adding `src/b<j>.txt` and taking its ids out of `unbuilt:` (citing it unless
    a Given made the commit uncited), and `plan.md` with its tasks, committed on main."""
    n, found = batch_name(step, name), step.context["given"]["batch"][name]
    items = [i for i, f in step.context["given"]["item"].items() if f["batch"] == name]
    tasks = [(t, f) for t, f in step.context["given"]["task"].items() if f["batch"] == name]
    give_batch_lines(step, items)
    W().init(step.repo)
    forked = git(step, "rev-parse", "HEAD").strip()
    git(step, "branch", n, forked)
    tree = outside(step) / n
    git(step, "worktree", "add", "-q", str(tree), n)
    lay(step, tree, items)
    git(step, "worktree", "remove", "--force", str(tree))
    commits = step.context.setdefault("commits", {})
    for item in items:
        b = B().ident(item)
        branch = "%s-%s" % (n, b)
        git(step, "branch", branch, n)
        tree = outside(step) / ("tree-%s" % branch)
        git(step, "worktree", "add", "-q", str(tree), branch)
        (tree / "src").mkdir(exist_ok=True)
        (tree / "src" / ("%s.txt" % b)).write_text("built %s\n" % b)
        built(tree, backlog_items.find(step.repo, b))
        git(step, "add", "-A", cwd=tree)
        mine = [c for c, f in step.context["given"].get("commit", {}).items() if f.get("item") == item]
        cited = not any(step.context["given"]["commit"][c].get("uncited") for c in mine)
        git(step, "commit", "-q", "-m", "build %s%s" % (b, "\n\nItem: %s" % b if cited else ""), cwd=tree)
        sha = git(step, "rev-parse", "HEAD", cwd=tree).strip()
        git(step, "worktree", "remove", "--force", str(tree))
        for c in mine or ["_%s" % item]:
            commits[c] = sha
    prs = [p for p, f in step.context["given"].get("pull request", {}).items() if f.get("batch") == name]
    status = "in-review" if prs else found.get("status", "building")
    url = URL % 1 if prs else None
    for p in prs:
        step.context.setdefault("prs", {})[p] = url
    rows = "".join("\n| %s | %s | %s | %s-%s |" % (task_id(step, t), B().ident(f["item"]), f["status"], n,
                                                      B().ident(f["item"])) for t, f in tasks)
    plan = step.repo / ".shop" / "batches" / n.split("-")[1] / "plan.md"
    plan.parent.mkdir(parents=True, exist_ok=True)
    plan.write_text("---\nid: batch/ex.com/prod/ctx/%s\nkind: batch\nstatus: %s\nbase: main\nforked_from: %s\n"
                    "branch: %s\npull_request:%s\n---\n\n# %s\n\n## Tasks\n\n| task | item | status | branch |\n"
                    "|---|---|---|---|%s\n\n## Plan\n\nThe world's batch.\n" % (
                        n, status, forked, n, " " + url if url else "", n, rows))
    W().init(step.repo)


def task_id(step, name):
    """The plan's `t<k>` of the scenario's task `name`, in the order the world numbers them."""
    ids = step.context.setdefault("task_ids", {})
    if name not in ids:
        ids[name] = "t%d" % (len(ids) + 1)
    return ids[name]


def plan_rel(step, name):
    return ".shop/batches/%s/plan.md" % batch_name(step, name).split("-")[1]


def plan_field(step, name, key):
    path = step.repo / plan_rel(step, name)
    return W().field(path, key) if path.is_file() else None


def task_row(step, name):
    """(status, branch) of the scenario's task `name` in its batch's plan."""
    found = step.context["given"]["task"][name]
    text = (step.repo / plan_rel(step, found["batch"])).read_text()
    row = re.search(r"^\| %s \| b\d+ \| (\S+) \| (\S+) \|$" % task_id(step, name), text, re.MULTILINE)
    return row.groups() if row else (None, None)


def run_batch(step, command, *args):
    """`work batch <command> <args>`, run in the repository after the world is prepared."""
    return B().run_work(step, "batch", command, *args, env=env(step), stdin=subprocess.DEVNULL, timeout=120)
