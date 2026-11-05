"""`work batch brief` (capability pr-review r3, r4; workflow simplification plan 5, D3-D8): what `pr-reviewer` reads
of a batch's pull request, written as `brief.md` and `change.diff` in the review's scratch directory under the ignored
worktrees directory, with nothing committed.

The first review (the pull request is unreviewed) reads the range `forked_from..head`: every commit of the batch and
no other, every requirement line of its in-batch items, the `tier: judgement` design-decisions, the rules
(`CLAUDE.md`), the size of the change and the runs of `[review] checks`, each with its command, exit code and output.
A re-review reads the range from the last review's head: the open findings, each with the commits for it, in place of
the items (r3 binds the first review only). Each check is also run once a batch at `forked_from`, and its exit code
there given beside the one at the head (review S5)."""
import json
import re
import shlex
import subprocess
from pathlib import Path

import backlog_items
import backlog_lines
import batch_findings
import batch_fix
import batch_plan
import workqueue
from batch_git import (
    SCRIPTS,
    current_branch,
    delivery,
    git,
    remote,
    remote_head,
    remove_tree,
    scripts_env,
    tree_for,
    trees_dir,
)
from workqueue import Refused

COMMAND = "work batch brief"
SIZE = 1000
CHECKS = ("python3 {scripts}/tools size --limit 300", "python3 {scripts}/tools check --base {forked_from}",
          "python3 {scripts}/features generate --check", "python3 {scripts}/features bindings --unbound")
TAIL = 40


def judgement(root):
    """(rel, summary) of each `spec/decisions/*.md` whose frontmatter has `tier: judgement` (D6)."""
    found = []
    for path in sorted((Path(root) / "spec" / "decisions").glob("*.md")):
        data, _ = workqueue.frontmatter(workqueue.read(path, root))
        if data.get("tier") == "judgement":
            found.append((path.relative_to(root).as_posix(), str(data.get("summary") or "").strip()))
    return found


def commits(root, rng, patches=None):
    """`<short sha> "<subject>" Item: b1 Finding: f1` of each commit of `rng`, oldest first, with `; patch: <path>`
    when `patches` has its own (review S4); a missing trailer is left out of its line."""
    out = git(root, "log", "--reverse", "--format=%h%x00%s%x00%(trailers:key=Item,valueonly,separator=%x2c)%x00"
              "%(trailers:key=Finding,valueonly,separator=%x2c)%x1e", rng).stdout
    lines = []
    for entry in filter(str.strip, out.split("\x1e")):
        sha, subject, item, finding = entry.strip("\n").split("\x00")
        line = "%s %s" % (sha, batch_findings.quoted(subject))
        for key, value in (("Item", item), ("Finding", finding)):
            if value.strip():
                line += " %s: %s" % (key, ", ".join(v.strip() for v in value.split(",") if v.strip()))
        lines.append(line + ("; patch: %s" % patches[sha] if sha in (patches or {}) else ""))
    return lines


def patches(tree, rng, where):
    """{short sha: path} of each non-merge commit of `rng`, its own change less `.shop/` written to
    `<where>/commits/<short sha>.patch` (review S4)."""
    folder = Path(where) / "commits"
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.glob("*.patch"):
        old.unlink()
    found = {}
    for sha in git(tree, "log", "--reverse", "--no-merges", "--format=%h", rng).stdout.split():
        found[sha] = folder / ("%s.patch" % sha)
        found[sha].write_text(git(tree, "show", "--format=commit %H%nAuthor: %an%n%n%B", sha, "--", ".",
                                  ":(exclude).shop").stdout, encoding="utf-8")
    return found


def size(root, rng):
    """(files, insertions, deletions) of the range, `.shop/` left out."""
    out = git(root, "diff", "--shortstat", rng, "--", ".", ":(exclude).shop").stdout
    counts = [int((re.search(r"(\d+) %s" % word, out) or [0, 0])[1]) for word in ("files? changed", "insertion",
                                                                                     "deletion")]
    return tuple(counts)


def head_of(brief_path, command=COMMAND):
    """The `Head:` the brief was written at."""
    for line in Path(brief_path).read_text(encoding="utf-8").splitlines():
        if line.startswith("Head: "):
            return line[len("Head: "):].strip()
    raise Refused("%s: %s has no Head: line; run work batch brief again" % (command, brief_path))


def _indented(text):
    return "\n".join("    %s" % line if line.strip() else "" for line in text.splitlines()) or "    (no output)"


def _run(command, where):
    return subprocess.run(shlex.split(command), cwd=where, capture_output=True, text=True, env=scripts_env())


def base_runs(root, batch, commands):
    """{command: exit code} of each check run at the batch's `forked_from`, in a throwaway worktree, once a batch:
    kept in the first review's scratch directory as `base-runs.json` (review S5, plan 5 rulings Q2)."""
    cache = batch_findings.scratch(root, batch.name, 1) / "base-runs.json"
    found = json.loads(cache.read_text(encoding="utf-8")) if cache.is_file() else {}
    missing = [c for c in commands if c not in found]
    if missing:
        tree = trees_dir(root) / ("%s-base" % batch.name)
        remove_tree(root, tree)
        git(root, "worktree", "add", "-q", "--detach", str(tree), batch.forked_from)
        try:
            found.update({c: _run(c, tree).returncode for c in missing})
        finally:
            remove_tree(root, tree)
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(found, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return found


def _runs(root, tree, batch):
    checks = delivery(root).get("review", {}).get("checks", list(CHECKS))
    if not isinstance(checks, list) or not all(isinstance(c, str) for c in checks):
        raise Refused("%s: .shop/delivery.toml: [review] checks is not a list of strings" % COMMAND)
    commands = [c.replace("{scripts}", str(SCRIPTS)).replace("{forked_from}", batch.forked_from) for c in checks]
    base, out = base_runs(root, batch, commands), []
    for command in commands:
        done = _run(command, tree)
        tail = "\n".join((done.stdout + done.stderr).splitlines()[-TAIL:])
        out.append("### `%s`\n\nExit code: %d (base: %d)\n\n%s" % (command, done.returncode, base[command],
                                                                       _indented(tail)))
    return "\n\n".join(out) or "none: [review] checks is empty"


def _items(root, batch):
    out = []
    for task in batch.tasks:
        item = backlog_items.find(root, task.item)
        if item.status != "in-batch":
            continue
        out.append("- %s: %s" % (backlog_items.label(item), backlog_items.rel_of(item.name)))
        for block in backlog_lines.read(item, backlog_items.rel_of(item.name)):
            for group in block.groups:
                out += ["  - %s#%s: %s" % (block.capability, rid, text) for rid, text in group.requirements]
    return "\n".join(out)


def _size(root, tree, rng):
    files, plus, minus = size(tree, rng)
    limit = delivery(root).get("review", {}).get("size", SIZE)
    said = "%d files, +%d -%d (limit %d changed lines)" % (files, plus, minus, limit)
    return said + ("; over the limit" if plus + minus > limit else "")


def _rules(tree):
    return ("`CLAUDE.md`: the repository's rules and module map, at %s" % (Path(tree) / "CLAUDE.md")
            if (Path(tree) / "CLAUDE.md").is_file() else "none: the repository has no CLAUDE.md")


def published(root, name, command=COMMAND):
    """The batch `name`, refused unless it is `in-review` with its pull request, `root` is on its base and its branch
    is at the remote's head of it."""
    batch = batch_plan.find(root, name)
    branch = current_branch(root)
    if branch != batch.base:
        raise Refused("%s: %s is built from %s; run it on %s, not %s" % (
            command, batch.name, batch.base, batch.base, branch or "a detached HEAD"))
    if batch.status != "in-review" or not batch.pull_request:
        raise Refused("%s: %s is %s; %s takes a batch that is in-review, with its pull request" % (
            command, batch.name, batch.status, command))
    head = git(root, "rev-parse", batch.branch).stdout.strip()
    if remote_head(root, remote(root, batch.base), batch.branch) != head:
        raise Refused("%s: %s is not at the remote's head of it; run work batch review %s, which pushes it" % (
            command, batch.branch, batch.name))
    return batch, head


def _header(batch, k, rng, head, tree, where, first):
    kind = "first; the pull request is unreviewed" if first else "re-review of the fix"
    return ["# The review of %s's pull request" % batch.name, "", "Review: %d (%s)" % (k, kind),
            "Batch: %s" % batch.name, "Pull request: %s" % batch.pull_request, "Base: %s" % batch.base,
            "Range: %s" % rng, "Head: %s" % head, "Tree: %s" % tree, "Findings file: %s" % (where / "findings.md")]


def _earlier(root, batch, own):
    """Each open finding with its text, its item's file and the commits for it, each with its patch (D5, S4)."""
    found, out = batch_fix.for_finding(root, batch), []
    for f in batch_findings.open_findings(root, batch.name):
        item = backlog_items.find(root, f.item)
        listed = ["  - %s%s" % (c, "; patch: %s" % own[c.split()[0]] if c.split()[0] in own else "")
                  for c in found.get(f.fid, [])]
        out.append("### %s %s %s: %s\n\n- item: %s, %s\n- where: %s\n- commits for it:\n%s%s" % (
            f.fid, f.grade, f.triage, f.title, backlog_items.label(item), backlog_items.rel_of(item.name),
            f.where or "-", "\n".join(listed) or "  - none",
            "\n\n%s" % f.body if f.body else ""))
    return "\n\n".join(out) or "none: no finding is open"


def brief(root, name):
    """(the brief's path, what was removed): `brief.md` and `change.diff` written for the batch's next review (D3)."""
    batch, head = published(root, name)
    done = batch_findings.reviews(root, batch.name)
    k, first = len(done) + 1, not done
    rng = "%s..%s" % (batch.forked_from if first else done[-1].head, head)
    tree = trees_dir(root) / batch.name
    tree_for(root, tree, batch.branch, COMMAND)
    where = batch_findings.scratch(root, batch.name, k)
    where.mkdir(parents=True, exist_ok=True)
    removed = []
    if (where / "findings.md").exists():
        (where / "findings.md").unlink()
        removed.append("findings.md")
    (where / "change.diff").write_text(git(tree, "diff", rng, "--", ".", ":(exclude).shop").stdout, encoding="utf-8")
    own = patches(tree, rng, where)
    decisions = judgement(root)
    sections = [("Items", _items(root, batch)) if first else ("Earlier findings", _earlier(root, batch, own)),
                ("Judgement decisions", "\n".join("- %s: %s" % d for d in decisions)
                 or "none: no design-decision is tier: judgement"),
                ("Rules", _rules(tree)), ("Size", _size(root, tree, rng)), ("Runs", _runs(root, tree, batch)),
                ("Commits", "\n".join("- %s" % c for c in commits(tree, rng, own)) or "none"),
                ("Change", "%s: `git diff %s -- . ':(exclude).shop'`" % (where / "change.diff", rng))]
    text = "\n".join(_header(batch, k, rng, head, tree, where, first)) + "".join(
        "\n\n## %s\n\n%s" % s for s in sections) + "\n"
    (where / "brief.md").write_text(text, encoding="utf-8")
    return where / "brief.md", removed
