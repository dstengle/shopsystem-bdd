"""`work batch brief` (capability pr-review r3, r4; workflow simplification plan 5, D3-D8): what `pr-reviewer` reads
of a batch's pull request, written as `brief.md` and `change.diff` in the review's scratch directory under the ignored
worktrees directory, with nothing committed.

The first review (the pull request is unreviewed) reads the range `forked_from..head`: every commit of the batch and
no other, every requirement line of its in-batch items, the `tier: judgement` design-decisions, the rules
(`CLAUDE.md`), the size of the change and the runs of `[review] checks`, each with its command, exit code and output.
A re-review reads the range from the last review's head: the open findings, each with the commits for it, in place of
the items (r3 binds the first review only)."""
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


def commits(root, rng):
    """`<short sha> "<subject>" Item: b1 Finding: f1` of each commit of `rng`, oldest first; a missing trailer is
    left out of its line."""
    out = git(root, "log", "--reverse", "--format=%h%x00%s%x00%(trailers:key=Item,valueonly,separator=%x2c)%x00"
              "%(trailers:key=Finding,valueonly,separator=%x2c)%x1e", rng).stdout
    lines = []
    for entry in filter(str.strip, out.split("\x1e")):
        sha, subject, item, finding = entry.strip("\n").split("\x00")
        line = '%s "%s"' % (sha, subject)
        for key, value in (("Item", item), ("Finding", finding)):
            if value.strip():
                line += " %s: %s" % (key, ", ".join(v.strip() for v in value.split(",") if v.strip()))
        lines.append(line)
    return lines


def size(root, rng):
    """(files, insertions, deletions) of the range, `.shop/` left out."""
    out = git(root, "diff", "--shortstat", rng, "--", ".", ":(exclude).shop").stdout
    counts = [int((re.search(r"(\d+) %s" % word, out) or [0, 0])[1]) for word in ("files? changed", "insertion",
                                                                                     "deletion")]
    return tuple(counts)


def head_of(brief_path):
    """The `Head:` the brief was written at."""
    for line in Path(brief_path).read_text(encoding="utf-8").splitlines():
        if line.startswith("Head: "):
            return line[len("Head: "):].strip()
    raise Refused("%s has no Head: line" % brief_path)


def _indented(text):
    return "\n".join("    %s" % line if line.strip() else "" for line in text.splitlines()) or "    (no output)"


def _runs(root, tree, batch):
    checks = delivery(root).get("review", {}).get("checks", list(CHECKS))
    if not isinstance(checks, list) or not all(isinstance(c, str) for c in checks):
        raise Refused("%s: .shop/delivery.toml: [review] checks is not a list of strings" % COMMAND)
    out = []
    for check in checks:
        command = check.replace("{scripts}", str(SCRIPTS)).replace("{forked_from}", batch.forked_from)
        done = subprocess.run(shlex.split(command), cwd=tree, capture_output=True, text=True, env=scripts_env())
        tail = "\n".join((done.stdout + done.stderr).splitlines()[-TAIL:])
        out.append("### `%s`\n\nExit code: %d\n\n%s" % (command, done.returncode, _indented(tail)))
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


def _earlier(root, batch):
    """Each open finding with its text, its item's file and the commits for it (D5)."""
    found, out = batch_fix.for_finding(root, batch), []
    for f in batch_findings.open_findings(root, batch.name):
        item = backlog_items.find(root, f.item)
        out.append("### %s %s %s: %s\n\n- item: %s, %s\n- where: %s\n- commits for it:\n%s%s" % (
            f.fid, f.grade, f.triage, f.title, backlog_items.label(item), backlog_items.rel_of(item.name),
            f.where or "-", "\n".join("  - %s" % c for c in found.get(f.fid, [])) or "  - none",
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
    decisions = judgement(root)
    sections = [("Items", _items(root, batch)) if first else ("Earlier findings", _earlier(root, batch)),
                ("Judgement decisions", "\n".join("- %s: %s" % d for d in decisions)
                 or "none: no design-decision is tier: judgement"),
                ("Rules", _rules(tree)), ("Size", _size(root, tree, rng)), ("Runs", _runs(root, tree, batch)),
                ("Commits", "\n".join("- %s" % c for c in commits(tree, rng)) or "none"),
                ("Change", "%s: `git diff %s -- . ':(exclude).shop'`" % (where / "change.diff", rng))]
    text = "\n".join(_header(batch, k, rng, head, tree, where, first)) + "".join(
        "\n\n## %s\n\n%s" % s for s in sections) + "\n"
    (where / "brief.md").write_text(text, encoding="utf-8")
    return where / "brief.md", removed
