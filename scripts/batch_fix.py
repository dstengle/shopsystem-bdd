"""The fix loop of a batch's pull request review (capability pr-review r6; workflow simplification plan 5, D11, D14):
a fix-now finding is fixed by commits on its item's branch, in its task's worktree, each citing `Item: b<j>` and
`Finding: f<m>`. `work batch review` checks them before it merges (`check`): every commit after the last review
cites an open finding of its item, and every open finding has a commit. `work batch resume` gives each open
finding's task its worktree back (`trees`) and prints where to fix it (`said`)."""
import backlog_items
import batch_findings
from batch_git import git, is_tree, tree_for, trees_dir
from workqueue import Refused


def cited_findings(root, since, branch):
    """(short sha, subject, finding ids) of each non-merge commit on `branch` after `since`, oldest first."""
    out = git(root, "log", "--reverse", "--no-merges", "--format=%h%x00%s%x00"
              "%(trailers:key=Finding,valueonly,separator=%x2c)%x1e", "%s..%s" % (since, branch)).stdout
    found = []
    for entry in filter(str.strip, out.split("\x1e")):
        sha, subject, cited = entry.strip("\n").split("\x00")
        found.append((sha, subject, {c.strip() for c in cited.replace(" ", ",").split(",") if c.strip()}))
    return found


def _last_head(root, batch):
    done = batch_findings.reviews(root, batch.name)
    return done[-1].head if done else None


def _branch(batch, finding):
    return next((t.branch for t in batch.tasks if t.item == finding.item), None)


def for_finding(root, batch):
    """{f<m>: [`<short sha> "<subject>"`, ...]}: the commits on each open finding's item branch after the last review
    that cite it."""
    since = _last_head(root, batch)
    found = {}
    for finding in batch_findings.open_findings(root, batch.name):
        branch = _branch(batch, finding)
        found[finding.fid] = ['%s "%s"' % (sha, subject) for sha, subject, cited in cited_findings(root, since, branch)
                              if finding.fid in cited] if since and branch else []
    return found


def _label(root, name):
    return backlog_items.label(backlog_items.find(root, name))


def check(root, batch, mine, command):
    """Refused unless every commit on an in-batch item's branch after the last review cites an open finding, and
    every open finding has a commit on its item's branch citing it (D11). A commit may cite another in-batch item's
    open finding, so that a branch may merge another's fix to resolve a conflict (plan 5 rulings, Q1). `mine` is
    [(task, item)] of the in-batch items."""
    since = _last_head(root, batch)
    if since is None:
        return
    still = batch_findings.open_findings(root, batch.name)
    allowed = {f.fid for f in still}
    named = ", ".join("%s (%s)" % (f.fid, f.item) for f in sorted(still, key=lambda f: int(f.fid[1:])))
    for task, item in mine:
        for sha, subject, cited in cited_findings(root, since, task.branch):
            if not cited & allowed:
                raise Refused('%s: %s: %s "%s" on %s cites no open finding (a Finding: f<m> line)%s' % (
                    command, batch.name, sha, subject, task.branch,
                    "; the open findings are %s" % named if named else
                    "; no finding is open: take the commit off %s" % task.branch))
    found = for_finding(root, batch)
    for finding in still:
        if not found.get(finding.fid):
            branch = _branch(batch, finding)
            raise Refused("%s: %s: %s %s (%s) has no commit citing it; fix it on %s with Finding: %s, or park %s" % (
                command, batch.name, finding.fid, _label(root, finding.item), finding.triage, branch, finding.fid,
                finding.item))


def trees(root, batch):
    """[(finding, task, worktree)] of each open finding, its task's worktree made again on its branch when it is lost
    (D14); the task's status is left as it is."""
    out = []
    for finding in batch_findings.open_findings(root, batch.name):
        task = next((t for t in batch.tasks if t.item == finding.item), None)
        if task is None:
            continue
        tree = trees_dir(root) / ("%s-%s" % (batch.name, task.task))
        if not is_tree(tree, task.branch):
            tree_for(root, tree, task.branch, "work batch resume")
        out.append((finding, task, tree))
    return out


def said(root, batch, found):
    """One line for each open finding: where and how to fix it (D14)."""
    return ["%s %s %s %s: %s: fix in %s on %s with Item: %s and Finding: %s; then work batch review %s" % (
        f.fid, f.grade, _label(root, f.item), f.where or "-", f.title, tree, task.branch, f.item, f.fid, batch.name)
        for f, task, tree in found]
